import sys
import pygame
from Components.Button import Button
from Menu import Menu
from Rain import Rain
from Utils.Events import EventType

GAMEOVER = False
clock = pygame.time.Clock()

def main():
    clock.tick(60)
    screen = Menu()
    
    while True:
        screen.update()

        for event in pygame.event.get():
            if event.type == EventType.START.value:
                del screen
                screen = Rain()
                
            elif event.type == EventType.GAMEOVER.value:
                del screen
                screen = Menu()
                
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        
        pygame.display.flip()


if __name__ == '__main__':
    main()
