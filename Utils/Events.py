from enum import Enum
import pygame

class EventType(Enum):
    START = pygame.event.custom_type()
    START_RAIN = pygame.event.custom_type()
    START_JOKENPO = pygame.event.custom_type()
    DAMAGE = pygame.event.custom_type()
    GAMEOVER = pygame.event.custom_type()