import os
import sys
import pygame
from Menu import Menu
from Rain import Rain
from Utils.Events import EventType

GAMEOVER = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 700))

def main():
    clock.tick(60)
    screen = Menu()

    while True:
        screen.update()
        ev_queue = pygame.event.get()
        # if ev_queue:
        #     print(ev_queue)

        for event in ev_queue:

            if event.type == EventType.START.value:
                screen.choose_game()
                pygame.event.clear()

            elif event.type == EventType.START_RAIN.value:
                del screen
                screen = Rain()

            elif event.type == EventType.START_JOKENPO.value:
                del screen

                pygame.quit()

                filename = 'JokenpoTeste.py'
                try:
                    os.system('python3.10 {}'.format(filename))
                except:
                    continue

                try:
                    os.system('python3 {}'.format(filename))
                except:
                    continue

            elif event.type == EventType.GAMEOVER.value:
                del screen
                screen = Menu()

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == '__main__':
    main()
