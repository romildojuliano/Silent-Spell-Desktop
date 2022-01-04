import math
import random
import cv2
import mediapipe as mp
import numpy as np
import pygame
import sys
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


class Player():

    def __init__(self, lifePoints=3) -> None:
        self.lifePoints = lifePoints
        self.fullLife = lifePoints
        self.score = 0

    def dec(self):
        # print(f'{self.lifePoints=}')
        self.lifePoints -= 1
        if self.lifePoints == 0:
            self.reset()
            print('--------------------GAME OVER--------------------')
            pygame.event.post(pygame.event.Event(EventType.GAMEOVER.value))

    def inc(self):
        self.lifePoints += 1

    def reset(self):
        self.lifePoints = self.fullLife
        self.score = 0


class Drop(pygame.sprite.Sprite):
    def __init__(self, image_path, screen, drop_group):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (30*3, 40*3))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

        for _ in range(50):
            self.rect.center = (
                random.randint(50, pygame.display.Info().current_w-50), random.randint(-100, 50))
            if not pygame.sprite.spritecollide(self, drop_group, False):
                break
        self.letter = random.choice(
            ["A", "B", "C", "D", "E", "I", "L", "M", "N", "O", "R", "S", "U", "V", "W"])
        self.font = self.font = pygame.font.SysFont('arial', 40)
        self.screen = screen
        self.safe = False

    def update(self, player):
        global score
        self.rect.center = (
            self.rect.center[0], self.rect.center[1] + 2 + player.score/100)
        draw_text(self.letter, self.font, (0, 0, 0), self.screen,
                  (self.rect.center[0], self.rect.center[1] + 20), True)

    def __del__(self):
        if(self.safe):
            pygame.event.post(pygame.event.Event(EventType.SCORE.value))
        else:
            pygame.event.post(pygame.event.Event(EventType.DAMAGE.value))


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
        pygame.init()

        pygame.display.set_caption('Rain Game')
        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w
        HEIGHT = infoObject.current_h
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont('arial', 30)

        self.player = Player(5)
        self.dropGroup = pygame.sprite.Group()
        self.groundGroup = pygame.sprite.Group()
        self.healthGroup = pygame.sprite.Group()
        self.ground = Ground()
        self.groundGroup.add(self.ground)
        health = [Heart(i) for i in range(self.player.fullLife)]
        for heart in health:
            self.healthGroup.add(heart)

        self.hands = mp_hands.Hands(
            min_detection_confidence=0.2, min_tracking_confidence=0.5, max_num_hands=1)
        self.cap = cv2.VideoCapture(0)
        self.model = load('silentSpellPrototipo.joblib')
        # self.lifePoints = PlayerHP(5)

    def __del__(self):
        self.hands.close()
        self.cap.release()

    def update(self):
        self.screen.fill((135, 206, 235))
        self.check_letter()
        self.add_drop()
        self.update_sprites()
        self.check_events()
        self.draw_score()

    def check_letter(self):
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

    def add_drop(self):
        if random.random() < min(self.player.score/1000 + 0.03, 0.5):
            drop = Drop("assets/Drop3.png", self.screen,
                        self.dropGroup)
            self.dropGroup.add(drop)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == EventType.DAMAGE.value:
                self.player.dec()
            if event.type == EventType.SCORE.value:
                self.player.score += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_sprites(self):
        self.dropGroup.draw(self.screen)
        self.dropGroup.update(self.player)
        self.groundGroup.draw(self.screen)
        pygame.sprite.spritecollide(self.ground, self.dropGroup, True)
        self.healthGroup.update(self.player)
        self.healthGroup.draw(self.screen)

    def draw_score(self):
        WIDTH, _ = self.screen.get_size()
        draw_text(f'Score: {self.player.score}', self.font,
                  (255, 255, 255), self.screen, (WIDTH - 100, 30), True)


class Heart(pygame.sprite.Sprite):
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

    def update(self, player):
        if player.lifePoints <= self.id:
            self.image = self.frames[1]


def draw_text(text, font, color, surface, position, center):
    textobj = font.render(text, 1, color)
    if center:
        textrect = textobj.get_rect(center=position)
    else:
        textrect = textobj.get_rect(topleft=position)
    surface.blit(textobj, textrect)
