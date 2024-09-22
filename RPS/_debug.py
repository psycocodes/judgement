import pygame

pygame.font.init()
font = pygame.font.SysFont(None, 20)
color = pygame.Color('white')


def debug(*args, **kwargs):
    win = pygame.display.get_surface()
    if args:
        win.blit(font.render(str([x for x in args]), 1, color, pygame.Color('black')), (0, 0))
    if kwargs:
        win.blit(font.render(str([f'{argument}={value}' for argument, value in kwargs.items()]), 1, color, pygame.Color('black')), (100, 0))

