import sys
import pygame
from typing import Tuple
from Components.Button import Button


pygame.init()

infoObject = pygame.display.Info()
WIDTH = infoObject.current_w // 2
HEIGHT = infoObject.current_h // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    global screen, font
    screen.fill((50, 50, 50))
    exit_btn = Button(screen, 'quit', 'arial', 20, (255, 255, 255),
                      (200, 0, 0), (WIDTH/2, HEIGHT/2), (60, 40), True, [pygame.quit, sys.exit])
    pygame.display.flip()
    while True:
        screen.fill((50, 50, 50))
        mouse = pygame.mouse.get_pos()
        exit_btn.draw(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                exit_btn.clicked(mouse)
        pygame.display.flip()

if __name__ == '__main__':
    main()
