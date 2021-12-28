import sys
import pygame
from Components.Button import Button
from typing import List
from Utils.Events import EventType


class Menu():
    buttons: List[Button]
    screen: pygame.surface.Surface

    def __init__(self):
        pygame.init()

        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w // 2
        HEIGHT = infoObject.current_h // 2
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        start_btn = Button(self.screen, 'Start', 'arial', 20, (255, 255, 255),
                           (200, 0, 0), (WIDTH//2, HEIGHT//3), (80, 60), True, [self.start_game])
        exit_btn = Button(self.screen, 'quit', 'arial', 20, (255, 255, 255),
                          (200, 0, 0), (WIDTH//2, HEIGHT//2), (80, 60), True, [pygame.quit, sys.exit])

        self.buttons = [start_btn, exit_btn]

    def start_game(self):
        pygame.event.post(pygame.event.Event(EventType.START.value))

    def destroy_all(self):
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
