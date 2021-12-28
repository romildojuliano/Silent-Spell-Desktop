from enum import Enum
import pygame

class EventType(Enum):
    START = pygame.event.custom_type()
