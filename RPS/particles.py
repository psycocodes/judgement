import pygame
import random
from RPS.particle_utils import load_preset

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (1, 1, 1)
BLUE = (0, 0, 255)
COLOR_KEY = (0, 0, 0)


def intensify(color, factor):
    return tuple(x + factor for x in color)


class Particle:
    def __init__(self, x, y, vx, vy, lifetime, color_set):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color_set = color_set
        self.lifetime = lifetime

    @property
    def pos_int(self):
        return int(self.x), int(self.y)

    def pos_transform(self, parameter):
        return self.pos_int[0] + parameter, self.pos_int[1] + parameter

    def draw(self, window, special_flags, properties):
        radius = self.lifetime  # Lifetime->Radius
        if properties['inner_circle']:
            pygame.draw.circle(window, color=self.color_set['primary'],
                               center=self.pos_int, radius=radius)
        if properties['outer_circle']:
            if properties['outer_circle_scale'] is not None:
                radius *= properties['outer_circle_scale']
            if properties['glow_intensity'] is not None:
                color = intensify(self.color_set['accent'], properties['glow_intensity'])
            else:
                color = self.color_set['accent']
            window.blit(self.circle_surf(radius=int(radius), color=color),
                        self.pos_transform(-radius), special_flags=special_flags)

    @staticmethod
    def circle_surf(radius, color):
        surface = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surface, color, (radius, radius), radius)  # (radius, radius)->Center of the Surface
        surface.set_colorkey(COLOR_KEY)
        surface.convert_alpha()
        return surface


class Particles:
    COLOR_SET = {'primary': WHITE,
                 'accent': GREY}
    PARTICLE_PROPERTIES = {'inner_circle': True,
                           'outer_circle': True,
                           'outer_circle_scale': 2,
                           'glow_intensity': 0
                           }

    def __init__(self, window=None,
                 pos=None, vx=1, vy=-1, gravity=0.00,
                 lifetime_min=5, lifetime_max=10, limit=60, end_radius=0, spread=0.001,
                 size_death_rate=0.08, alpha_death_rate=0,
                 color_set=None,
                 optimization_factor=1,
                 properties=None,
                 special_flags=None):

        self.window = window if window is not None else pygame.display.get_surface()

        pos = pos if pos is not None else (
        pygame.display.get_surface().get_width() // 2, pygame.display.get_surface().get_height() // 2)
        self.x = pos[0]
        self.y = pos[1]
        self.vx = vx
        self.vy = vy
        self.gravity = gravity

        # Optimization Factor<->Intensity Factor
        self.frames = 0
        self.optimization_factor = optimization_factor if type(1) == type(optimization_factor) and optimization_factor != 1 else 1
        self.color_set = Particles.COLOR_SET | color_set  if color_set is not None else Particles.COLOR_SET

        self.lifetime = lifetime_min, lifetime_max
        self.limit = limit
        self.end_radius = end_radius
        self.spread = spread
        self.size_death_rate = size_death_rate
        self.alpha_death_rate = alpha_death_rate

        self.special_flags = special_flags if special_flags is not None else pygame.BLEND_RGBA_ADD
        self.properties = Particles.PARTICLE_PROPERTIES | properties if properties is not None else Particles.PARTICLE_PROPERTIES

        self.particles = []  # Particle -> [Position, Velocity, Lifetime, Color]

    def render(self):
        if self.frames % self.optimization_factor == 0:
            self.frames = 0
            if len(self.particles) <= self.limit:
                particle = Particle(self.x, self.y, self.vx, self.vy, self.lifetime, self.color_set)
                particle.lifetime = random.randint(*self.lifetime)
                particle.vx = (random.randint(0, int(particle.vx)) / (particle.vx / self.spread)) - (self.spread / 2) if self.spread != 0 else particle.vx
                particle.vy = particle.vy
                self.particles.append(particle)

        for particle in self.particles:
            particle.x += particle.vx
            particle.y += particle.vy
            particle.vy += self.gravity
            particle.lifetime -= self.size_death_rate
            particle.draw(self.window, self.special_flags, self.properties)
            if self.size_death_rate >= 0:
                if particle.lifetime <= self.end_radius:
                    self.particles.remove(particle)
            else:
                if particle.lifetime >= self.end_radius:
                    self.particles.remove(particle)

        # Debug
        # pygame.draw.rect(self.window, 'yellow', pygame.Rect((self.x-40, self.y-40),(80,80)), 2, 0)
        self.frames += 1

class ParticleManager:
    def __init__(self, window, data, file_path):
        self.window = window
        self.data = data
        self.particles = {}
        self.file_path = file_path
        self.init_particles()

    def init_particles(self):
        for index, data in self.data.items():
            for p_type, position in data.items():
                self.particles[index] = Particles(self.window, position, **load_preset(self.file_path, p_type))

    def render(self):
        self.update()
        for particles in self.particles.values():
            particles.render()

    def scalar_add(self, scalar=0):
        for particles in self.particles.values():
            particles.x += scalar
            particles.y += scalar

    def update(self):
        pass




