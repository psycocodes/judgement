import pygame
import random
class Vignette:
    RADIUS = 100

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.radius = Vignette.RADIUS
        self.brightness = 6
        self.bleed = 140
        self.feather = 10
        self.anim_v = 0.0
        self.anim_d = 1
        self.min_brightness = 6
        self.max_brightness = 10

    def render(self, display: pygame.Surface, window):
        self.update()
        surface = pygame.Surface((self.radius*2, self.radius*2))
        # surface.fill((0, 0, 0))
        for i in range(0, 256, self.feather):
            pygame.draw.circle(surface, (i, i, i), surface.get_rect().center, self.radius - i / self.brightness)

        display.blit(pygame.transform.scale(surface, [x+self.bleed for x in display.get_size()]), (-self.bleed//2, -self.bleed//2))
        window.blit(pygame.transform.scale(display, window.get_size()),
                         (self.x, self.y), special_flags=pygame.BLEND_MULT)

    def update(self):
        if self.brightness >= self.max_brightness:
            self.anim_d = -1
        elif self.brightness <= self.min_brightness:
            self.anim_d = 1
        self.brightness += self.anim_v*self.anim_d


class Fade:
    def __init__(self, speed=3, direction=-1):
        self.alpha = 0 if direction >= 0 else 255
        self.speed = speed
        self.direction = direction

    def render(self, display, window):
        self.update()
        surface = pygame.Surface(display.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, self.alpha))
        window.blit(pygame.transform.scale(surface, window.get_size()), (0, 0))

    def update(self):
        if self.direction > 0:
            if self.alpha < 255:
                self.alpha += self.speed*self.direction
                if self.alpha == 255-255 % 6:
                    self.alpha = 255
        else:
            if self.alpha > 0:
                self.alpha += self.speed*self.direction
                if self.alpha < 0:
                    self.alpha = 0
