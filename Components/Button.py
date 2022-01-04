from typing import Tuple
import pygame


class Button():
    position: Tuple[int, int]
    text_pos: Tuple[int, int]
    size: Tuple[int, int]
    screen: pygame.surface.Surface
    font: pygame.font.Font
    text_color: Tuple[int, int, int]
    button_color: Tuple[int, int, int]
    center: bool

    def __init__(self, screen, text, font, font_size, text_color, button_color, position, center, events):
        self.screen = screen
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.text_color = text_color
        self.button_color = button_color
        self.size = self.get_size(text)
        self.center = center
        self.set_pos(position)
        self.events = events

    def set_pos(self, position):
        if self.center:
            self.position = (position[0] - self.size[0]//2,
                             position[1] - self.size[1]//2)
        else:
            self.position = position

        self.text_pos = (self.position[0] + self.size[0]//2,
                         self.position[1] + self.size[1]//2)

        self.rect = pygame.Rect(self.position, self.size)

    def get_size(self, text):
        text_obj = self.font.render(text, 1, (0, 0, 0))
        text_rect = text_obj.get_rect()
        return (text_rect[2]+25, text_rect[3]+25)

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mx, my):
            pygame.draw.rect(self.screen, self.button_color, self.rect)
        else:
            off_color = (int(self.button_color[0]*.8),
                         int(self.button_color[1]*.8),
                         int(self.button_color[2]*.8),
                         0)
            pygame.draw.rect(self.screen, off_color, self.rect)

        draw_text(self.text, self.font, self.text_color,
                  self.screen, self.text_pos, True)

    def clicked(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            for event in self.events:
                event()


def draw_text(text, font, color, surface, position, center):
    text_obj = font.render(text, 1, color)
    if center:
        text_rect = text_obj.get_rect(center=position)
    else:
        text_rect = text_obj.get_rect(topleft=position)
    surface.blit(text_obj, text_rect)
