import sys
import pygame
from Components.Button import Button
from typing import List
from Utils.Events import EventType

class Menu():
    buttons: List[Button]
    screen: pygame.surface.Surface
    dimensions: dict

    def __init__(self):
        pygame.init()

        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w 
        HEIGHT = infoObject.current_h
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        start_btn = Button(self.screen, 'Start', 'arial', 20, (255, 255, 255),
                           (200, 0, 0), (WIDTH//2, HEIGHT//3), (80, 60), True, [self.start_game])
        exit_btn = Button(self.screen, 'quit', 'arial', 20, (255, 255, 255),
                          (200, 0, 0), (WIDTH//2, HEIGHT//2), (80, 60), True, [self.quit_game])

        self.buttons = [start_btn, exit_btn]
        self.dimensions = {'width': WIDTH, 
                           'height': HEIGHT}

    def start_game(self):
        pygame.event.post(pygame.event.Event(EventType.START.value))
        
    def choose_game(self):
        self.screen = pygame.display.set_mode((self.dimensions['width'], self.dimensions['height']))
        rain_button = Button(self.screen, 'Rain Game', 'arial', 20, (255, 255, 255),
                           (200, 0, 0), (self.dimensions['width']//2, self.dimensions['height']//3), (80, 60), True, [self.start_rain_game])
        jokenpo_button = Button(self.screen, 'Jokenpo', 'arial', 20, (255, 255, 255),
                          (200, 0, 0), (self.dimensions['width']//2, self.dimensions['height']//2), (80, 60), True, [self.start_jokenpo])
        self.buttons = [rain_button, jokenpo_button]

    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def start_rain_game(self):
        pygame.event.post(pygame.event.Event(EventType.START_RAIN.value))
    
    def start_jokenpo(self):
        pygame.event.post(pygame.event.Event(EventType.START_JOKENPO.value))

    def __del__(self):
        for btn in self.buttons:
            del btn

    def update(self):
        self.screen.fill((50, 50, 50))
        for btn in self.buttons:
            btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    btn.clicked()
