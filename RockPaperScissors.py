import pygame
from Utils.Events import EventType
import Utils.HandsHandler as HH
import Utils.Utils as Utils

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
        self.frames = 0
        player.reset()

        self.hands = HH.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1)
        self.cap = HH.cv2.VideoCapture(0)
        self.model = HH.load('pedraPapelTesoura.joblib') 
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
    
        Utils.draw_text(f'Vida: {player.lifePoints}', self.font, (255,255,255),self.screen, (0,0), False)
        
