import sys
import pygame
from Components.Button import Button
from Menu import Menu
from Utils.Events import EventType


def main():
    state = 0
    menu = Menu()
    while True:
        match state:
            case 0:
                menu.update()
            case 1:
                # jogo
                pass

        for event in pygame.event.get():
            print('minha pica')
            if event.type == EventType.START.value:
                state = 1
                menu.destroy_all()
                menu.update()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == '__main__':
    main()
