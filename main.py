import sys
import pygame
from Components.Button import Button
from Menu import Menu
from Rain import Rain
from Utils.Events import EventType


def main():
    state = 0
    screen = Menu()
    
    while True:

        screen.update()
        for event in pygame.event.get():
            if event.type == EventType.START.value:
                state = 1
                del screen
                screen = Rain()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == '__main__':
    main()
