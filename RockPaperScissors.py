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
        self.lifePoints -= 1
    
    def inc(self):
        self.lifePoints += 1

    def reset(self):
        self.lifePoints = self.fullLife
    
player = PlayerHP(3)

pedra = pygame.transform.scale(pygame.image.load("assets/pedra.png"),(30*5,40*5))
papel = pygame.transform.scale(pygame.image.load("assets/papel.png"),(30*5,40*5))
tesoura = pygame.transform.scale(pygame.image.load("assets/tesoura.png"),(30*5,40*5))
       

class rockPaperScissors():
    screen: pygame.surface.Surface

    def __init__(self):
        global player, font
        pygame.init()
        self.font = pygame.font.SysFont('arial', 30)
        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w 
        HEIGHT = infoObject.current_h 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        player.reset()

        self.hands = HH.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1)
        self.cap = HH.cv2.VideoCapture(0)
        self.model = HH.load('pedraPapelTesoura.joblib')
        self.start_ticks=pygame.time.get_ticks() 
        self.gameON = True
        # self.lifePoints = PlayerHP(5)
        
    def __del__(self):
        self.hands.close()
        self.cap.release()

    def update(self):

        global player
        self.screen.fill((0, 50, 255))
        
        image, choosenOption = HH.apllyMediaPipe(self.cap,self.hands,self.model)

        self.screen.blit(pygame.surfarray.make_surface(image),(200,100))
        if choosenOption:
            if choosenOption == 'Pedra':
                self.screen.blit(pedra, (100,100))
            elif choosenOption == 'Papel':
                self.screen.blit(papel, (100,100))
            elif choosenOption == 'Tesoura':
                self.screen.blit(tesoura, (100,100))
        
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000
        Utils.draw_text(str(seconds), self.font, (255,0,0),self.screen, (100,100), False)
        if seconds >=15 and not self.gameON:
            self.gameON = True
            self.start_ticks=pygame.time.get_ticks() 
        elif seconds >= 10:
            if self.gameON:
                self.gameON = False
                self.enemyOption = random.choice(['Pedra','Papel','Tesoura'])
                self.choosenOption = choosenOption
            else:
                if self.enemyOption == 'Pedra':
                    self.screen.blit(pedra, (1000,100))
                    if self.choosenOption == 'Pedra':
                        Utils.draw_text("draw", self.font, (255,255,255),self.screen, (500,100), False)
                        self.screen.blit(pedra, (100,100))
                    elif self.choosenOption == 'Papel':
                        Utils.draw_text("win", self.font, (255,255,255),self.screen, (500,100), False)
                        self.screen.blit(papel, (100,100))
                    elif self.choosenOption == 'Tesoura':
                        self.screen.blit(tesoura, (100,100))
                        Utils.draw_text("Lose", self.font, (255,255,255),self.screen, (500,100), False)
                if self.enemyOption == 'Papel':
                    self.screen.blit(papel, (1000,100))
                    if self.choosenOption == 'Papel':
                        self.screen.blit(papel, (100,100))
                        Utils.draw_text("draw", self.font, (255,255,255),self.screen, (500,100), False)
                    elif self.choosenOption == 'Tesoura':
                        self.screen.blit(tesoura, (100,100))
                        Utils.draw_text("win", self.font, (255,255,255),self.screen, (500,100), False)
                    elif self.choosenOption == 'Pedra':
                        self.screen.blit(pedra, (100,100))
                        Utils.draw_text("Lose", self.font, (255,255,255),self.screen, (500,100), False)
                if self.enemyOption == 'Tesoura':
                    self.screen.blit(tesoura, (1000,100))
                    if self.choosenOption == 'Tesoura':
                        self.screen.blit(tesoura, (100,100))
                        Utils.draw_text("draw", self.font, (255,255,255),self.screen, (500,100), False)
                    elif self.choosenOption == 'Pedra':
                        self.screen.blit(pedra, (100,100))
                        Utils.draw_text("win", self.font, (255,255,255),self.screen, (500,100), False)
                    elif self.choosenOption == 'Papel':
                        self.screen.blit(papel, (100,100))
                        Utils.draw_text("Lose", self.font, (255,255,255),self.screen, (500,100), False)
        
        

        Utils.draw_text(f'Vida: {player.lifePoints}', self.font, (255,255,255),self.screen, (0,0), False)
        
