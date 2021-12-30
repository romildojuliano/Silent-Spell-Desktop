def draw_text(text, font, color, surface, position, center):
    textobj = font.render(text, 1, color)
    if center:
        textrect = textobj.get_rect(center = position)
    else:
        textrect = textobj.get_rect(topleft = position)
    surface.blit(textobj, textrect)