from typing import Tuple
import pygame

infoObject = pygame.display.Info()
WIDTH = infoObject.current_w // 2
HEIGHT = infoObject.current_h // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Button():
    position: Tuple[int, int]
    text_pos: Tuple[int, int]
    size: Tuple[int, int]
    screen: pygame.surface.Surface
    font: pygame.font.Font
    text_color: Tuple[int, int, int]
    button_color: Tuple[int, int, int]
    center: bool

    def __init__(self, screen, text, font, font_size, text_color, button_color, position, size, center, events):
        self.screen = screen
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.text_color = text_color
        self.button_color = button_color
        if center:
            self.position = (position[0] - size[0]//2,
                             position[1] - size[1]//2)
        else:
            self.position = position
        self.size = size
        self.text_pos = (self.position[0] + self.size[0]//2,
                         self.position[1] + self.size[1]//2)
        self.center = center
        self.events = events


    def mouse_in_range(self, mouse_pos) -> bool:
        x, y = self.position
        width, height = self.size
        mouse_x, mouse_y = mouse_pos

        return x <= mouse_x <= x + width and y <= mouse_y <= y + height


    def draw(self, mouse_pos):
        rect = self.position + self.size

        if not self.mouse_in_range(mouse_pos):
            pygame.draw.rect(screen, self.button_color, rect=rect)
        else:
            off_color = (int(self.button_color[0]*.8),
                         int(self.button_color[1]*.8),
                         int(self.button_color[2]*.8),
                         0)
            pygame.draw.rect(screen, off_color, rect=rect)

        draw_text(self.text, self.font, self.text_color,
                  self.screen, self.text_pos)

    def clicked(self, mouse_pos):
        if self.mouse_in_range(mouse_pos):
            for event in self.events:
                event()


def draw_text(text, font, color, surface, position):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=position)
    surface.blit(textobj, textrect)