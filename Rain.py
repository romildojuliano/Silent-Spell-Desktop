from random import randint
import pygame
from Utils.Events import EventType
import Utils.HandsHandler as HH
import Utils.Utils as Utils
import random

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
    
player = PlayerHP(50)

class Drop(pygame.sprite.Sprite):
    def __init__(self,image_path, screen):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path),(30*5,40*5))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.center = (randint(50,pygame.display.Info().current_w-50),50)
        self.letter = random.choice(["A","B","C","D","E","I","L","M","N","O","R","S","U","V","W"])
        self.font = self.font = pygame.font.SysFont('arial', 60)
        self.screen = screen
        self.safe = False
        

    def update(self):    
        self.rect.center = (self.rect.center[0],self.rect.center[1]+2)
        Utils.draw_text(self.letter, self.font, (0,0,0), self.screen, (self.rect.center[0], self.rect.center[1]+30), True)

    def __del__(self):
        global player
        if(not self.safe):
            player.dec()
            if player.lifePoints == 0:
                print('--------------------GAME OVER-------------------')
                pygame.event.post(pygame.event.Event(EventType.GAMEOVER.value))
    
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        infoObject = pygame.display.Info()
        self.image = pygame.Surface([infoObject.current_w,50])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (infoObject.current_w//2,infoObject.current_h+10)
        

class Rain():
    screen: pygame.surface.Surface

    def __init__(self):
        global player, font
        pygame.init()
        self.font = pygame.font.SysFont('arial', 30)
        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w #// 2 esse 2 é necessario? tive que tirar por que tava bugando....
        HEIGHT = infoObject.current_h #// 2
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.dropGroup = pygame.sprite.Group()
        self.groundGroup = pygame.sprite.Group()
        self.ground = Ground()
        self.groundGroup.add(self.ground)
        self.frames = 0
        player.reset()

        self.hands = HH.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1)
        self.cap = HH.cv2.VideoCapture(0)
        self.model = HH.load('silentSpellPrototipo.joblib') 
        # self.lifePoints = PlayerHP(5)
        
    def __del__(self):
        self.hands.close()
        self.cap.release()

    def update(self):

        self.frames += 1
        global player
        self.screen.fill((0, 50, 255))
        
        image, choosenLetter = HH.apllyMediaPipe(self.cap,self.hands,self.model)

        
        self.screen.blit(pygame.surfarray.make_surface(image),(200,100))
        if choosenLetter:
            Utils.draw_text(choosenLetter, self.font, (255,255,255),self.screen, (100,100), False)
            for drop in self.dropGroup:
                    if drop.letter == choosenLetter:
                        drop.safe = True
                        drop.kill()
        self.dropGroup.draw(self.screen)
        if self.frames % 100 == 0:
            # print(2)
            drop = Drop("assets/Drop3.png", self.screen)
            self.dropGroup.add(drop)
            
        self.groundGroup.draw(self.screen)
        self.dropGroup.update()
        pygame.sprite.spritecollide(self.ground,self.dropGroup,True)
        Utils.draw_text(f'Vida: {player.lifePoints}', self.font, (255,255,255),self.screen, (0,0), False)
        

class hpBar():
    def __init__(self) -> None:
        pass
        
    pass
        
