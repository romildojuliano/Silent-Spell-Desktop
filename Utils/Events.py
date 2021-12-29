from enum import Enum
import pygame

class EventType(Enum):
    START = pygame.event.custom_type()
    DAMAGE = pygame.event.custom_type()
    GAMEOVER = pygame.event.custom_type()