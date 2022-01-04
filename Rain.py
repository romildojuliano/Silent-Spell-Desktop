import math
import random
import cv2
import mediapipe as mp
import numpy as np
import pygame
from joblib import load
from Utils.Events import EventType

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def subLandmarks(v1, v2):
    return [v1.x-v2.x, v1.y-v2.y, v1.z-v2.z]


def angle(s, c, e):
    Js = subLandmarks(s, c)
    #Jc = subLandmarks(c,c)
    Je = subLandmarks(e, c)
    return math.acos(np.inner(Js, Je)/(math.sqrt(np.inner(Js, Js))*math.sqrt(np.inner(Je, Je))))


class PlayerHP():

    def __init__(self, lifePoints=3) -> None:
        self.lifePoints = lifePoints
        self.fullLife = lifePoints

    def dec(self):
        # print(f'{self.lifePoints=}')
        self.lifePoints -= 1

    def inc(self):
        self.lifePoints += 1

    def reset(self):
        self.lifePoints = self.fullLife


player = PlayerHP(5)
score = 0

class Drop(pygame.sprite.Sprite):
    def __init__(self, image_path, screen):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (30*5, 40*5))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.center = (
            random.randint(50, pygame.display.Info().current_w-50), 50)
        self.letter = random.choice(
            ["A", "B", "C", "D", "E", "I", "L", "M", "N", "O", "R", "S", "U", "V", "W"])
        self.font = self.font = pygame.font.SysFont('arial', 60)
        self.screen = screen
        self.safe = False

    def update(self):
        self.rect.center = (self.rect.center[0], self.rect.center[1]+2)
        draw_text(self.letter, self.font, (0, 0, 0), self.screen,
                  (self.rect.center[0], self.rect.center[1]+30), True)

    def __del__(self):
        global player, score
        if(self.safe):
            score += 1
        else:
            player.dec()
            if player.lifePoints == 0:
                print('--------------------GAME OVER-------------------')
                score = 0
                pygame.event.post(pygame.event.Event(EventType.GAMEOVER.value))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        infoObject = pygame.display.Info()
        self.image = pygame.Surface([infoObject.current_w, 50])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (infoObject.current_w//2, infoObject.current_h+10)


class Rain():
    screen: pygame.surface.Surface

    def __init__(self):
        global player, font
        pygame.init()
        self.font = pygame.font.SysFont('arial', 30)
        infoObject = pygame.display.Info()
        # // 2 esse 2 é necessario? tive que tirar por que tava bugando....
        WIDTH = infoObject.current_w
        HEIGHT = infoObject.current_h  # // 2
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Rain Game')
        self.dropGroup = pygame.sprite.Group()
        self.groundGroup = pygame.sprite.Group()
        self.healthGroup = pygame.sprite.Group()
        self.ground = Ground()
        self.groundGroup.add(self.ground)
        self.health = [hpBar(i) for i in range(player.fullLife)]
        for heart in self.health:
            self.healthGroup.add(heart)
        player.reset()

        self.hands = mp_hands.Hands(
            min_detection_confidence=0.2, min_tracking_confidence=0.5, max_num_hands=1)
        self.cap = cv2.VideoCapture(0)
        self.model = load('silentSpellPrototipo.joblib')
        # self.lifePoints = PlayerHP(5)

    def __del__(self):
        self.hands.close()
        self.cap.release()

    def update(self):

        global player
        self.screen.fill((135 , 206, 235))

        if(self.cap.isOpened()):
            success, image = self.cap.read()
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                points = []
                trincas = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [5, 6, 7], [6, 7, 8], [9, 10, 11], [10, 11, 12], [
                    13, 14, 15], [14, 15, 16], [17, 18, 19], [18, 19, 20], [8, 0, 20], [12, 0, 20], [4, 0, 16], [16, 0, 20]]
                landmarks = list(results.multi_hand_landmarks[0].landmark)
                for trinca in trincas:
                    a = angle(landmarks[trinca[0]],
                              landmarks[trinca[1]], landmarks[trinca[2]])
                    points.append(a)
                choosenLetter = self.model.predict([points])[0]
                draw_text(choosenLetter, self.font, (255, 255, 255),
                          self.screen, (100, 100), False)
                for drop in self.dropGroup:
                    if drop.letter == choosenLetter:
                        drop.safe = True
                        drop.kill()
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            image = cv2.flip(image, 1)
            image = cv2.resize(image, self.screen.get_size())
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = np.rot90(image)
            self.screen.blit(pygame.surfarray.make_surface(image), (0, 0))

        self.dropGroup.draw(self.screen)
        if score < 900 and random.random() < score/1000 + 0.1:
            drop = Drop("assets/Drop3.png", self.screen)
            self.dropGroup.add(drop)

        self.groundGroup.draw(self.screen)
        self.dropGroup.update()
        pygame.sprite.spritecollide(self.ground, self.dropGroup, True)

        self.healthGroup.update()
        self.healthGroup.draw(self.screen)
        WIDTH, HEIGHT = self.screen.get_size()
        draw_text(f'Score: {score}', self.font,
                  (255, 255, 255), self.screen, (WIDTH - 100, 30), True)


class hpBar(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.frames = []
        scale = 1
        self.sprite_sheet = pygame.transform.scale(
            pygame.image.load('assets/health2.png'), (136*scale, 60*scale))

        for i in range(2):
            img = self.sprite_sheet.subsurface((i * 68, 0), (68, 60))
            self.frames.append(img)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (id * 68, 10)
        self.id = id

    def update(self):
        if player.lifePoints <= self.id:
            self.image = self.frames[1]


def draw_text(text, font, color, surface, position, center):
    textobj = font.render(text, 1, color)
    if center:
        textrect = textobj.get_rect(center=position)
    else:
        textrect = textobj.get_rect(topleft=position)
    surface.blit(textobj, textrect)
