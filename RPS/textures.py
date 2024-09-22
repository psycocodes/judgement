import pygame
import os

pygame.font.init()

fonts = {"f_1": "RETRO_SPACE.ttf", "f_2": "RETRO_SPACE_INV.ttf"}


def texture_resize(texture, factor):
    ratio = texture.get_width(), texture.get_height()
    size = int(factor*ratio[0]), int(factor*ratio[1])
    return pygame.transform.scale(texture, size)


def font_render(file_code, size=40):
    return pygame.font.Font(os.path.join('Assets', fonts[file_code]), size)


factor1 = 0.4


def import_bg(width, height, factor=(0, 0)):
    t_bg = pygame.transform.scale(pygame.image.load(os.path.join('RPS/Assets', 'bg.png')), (width+factor[0], height+factor[1]))
    return t_bg


def blit_asset(display, texture: pygame.Surface, coordinates=(0, 0), special_flags=0):
    try:
        display.blit(texture, coordinates, special_flags=special_flags)
    except FileNotFoundError:
        pygame.draw.rect(display, 'purple', pygame.Rect(coordinates, (40, 40)))


def texture_load(name, parent_dir='RPS', file_ext='png'):
    return pygame.image.load(os.path.join(f'{parent_dir}/Assets', f'{name}.{file_ext}'))

def dynamic_texture(texture, size, factor=1):
    return pygame.transform.scale(texture, (size[0]*factor, size[1]*factor))

