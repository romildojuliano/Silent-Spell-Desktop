from random import randint
import sys
import pygame
from Components.Button import Button
from typing import List
from Utils.Events import EventType

class PlayerHP:
    lifePoints: int
    
    def __init__(self, lifePoints=3) -> None:
        self.lifePoints = lifePoints

    def dec(self):
        self.lifePoints -= 1
    
    def inc(self):
        self.lifePoints += 1
    

class Drop(pygame.sprite.Sprite):
    def __init__(self,image_path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path),(30,40))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.center = [randint(50,pygame.display.Info().current_w-50),50]

    def update(self):    
        self.rect.center = [self.rect.center[0],self.rect.center[1]+1]
    
    def __del__(self):
        pygame.event.post(pygame.event.Event(EventType.DAMAGE.value))
    
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        infoObject = pygame.display.Info()
        self.image = pygame.Surface([infoObject.current_w,50])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = [infoObject.current_w//2,infoObject.current_h+10]

class Rain():
    screen: pygame.surface.Surface

    def __init__(self):
        pygame.init()

        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w #// 2 esse 2 é necessario? tive que tirar por que tava bugando....
        HEIGHT = infoObject.current_h #// 2
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.dropGroup = pygame.sprite.Group()
        self.groundGroup = pygame.sprite.Group()
        self.ground = Ground()
        self.groundGroup.add(self.ground)
        self.lifePoints = PlayerHP(5)
        
    def __del__(self):
        pass

    def update(self):
        self.screen.fill((0, 50, 255))
        self.dropGroup.draw(self.screen)
        drop = Drop("assets/Drop3.png")
        self.dropGroup.add(drop)
        self.dropGroup.update()
        self.groundGroup.draw(self.screen)
        pygame.sprite.spritecollide(self.ground,self.dropGroup,True)
        for event in pygame.event.get():
            if event.type == EventType.DAMAGE.value:
                self.lifePoints.dec()
                print(self.lifePoints.lifePoints)
            
        if self.lifePoints.lifePoints == 0:
            pygame.event.post(pygame.event.Event(EventType.GAMEOVER.value))
            print("Alterei o gameState!")
            

class hpBar():
    def __init__(self) -> None:
        pass
        
    pass
        
