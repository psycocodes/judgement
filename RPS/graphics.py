import pygame
import sys
from RPS.logic import Logic
from RPS._debug import debug
from RPS.constants import WINDOW_FACTOR, DATA_FILE_PATH, PRESET_FILE_PATH, SCROLL, SCROLL_VX
from RPS.textures import *
from RPS.particles import ParticleManager
from copy import copy
from RPS.particle_utils import load_data
from RPS.vfx import Vignette, Fade


class Graphics:
    DISPLAY_SCALE = 2  # Display_scale refers to the scaled down size of the display which is scaled up again
    WINDOW_FACTOR = WINDOW_FACTOR / 100
    SCROLL = SCROLL
    SCROLL_VX = SCROLL_VX
    colordict = {'rock': 'green',
                 'paper': 'yellow',
                 'scissors': 'cyan',
                 'lizard': 'red',
                 'spock': 'orange'}

    def __init__(self, FPS=60):
        self._init(FPS)
        # Game Initialisation
        self.game_logic = Logic()
        self.initial_time = 0
        self.final_time = 0
        self.delta_time = self.final_time - self.initial_time
        self.cooldown = False
        self.cooldown_table = {'round': 2000,
                               'end': 5000}
        self.cooldown_type = 'round'  # By Default
        self.cooldown_time = self.cooldown_table[self.cooldown_type]
        self.particle_surface = pygame.Surface((self.width // Graphics.DISPLAY_SCALE, self.height // Graphics.DISPLAY_SCALE))
        self.particles_m = ParticleManager(self.particle_surface, load_data(DATA_FILE_PATH), PRESET_FILE_PATH)
        self.vignette_surface = self.window_s.copy()
        self.fade_surface = self.display.copy()
        self.fade = Fade(2, -1)
        self.vignette = Vignette((0, 0))

        self.scroll = -Graphics.SCROLL
        self.scroll_vx = Graphics.SCROLL_VX
        self.screen_bleed_h = self.screen_bleed_w = 10
        self.color = 'green'
        self.color2 = 'white'

        self.screen_factor = [1, 1]

    def _init(self, FPS):
        pygame.init()
        self.monitor_size = self.monitor_width, self.monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.size = self.width, self.height = self.monitor_width * Graphics.WINDOW_FACTOR, self.monitor_height * Graphics.WINDOW_FACTOR
        self.window = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.window_s = pygame.Surface(self.size)
        pygame.display.set_caption('Game')
        self.display = pygame.Surface((self.width // Graphics.DISPLAY_SCALE, self.height // Graphics.DISPLAY_SCALE))
        self.display.set_colorkey((0, 0, 0))
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.fullscreen_cooldown = False
        self.fullscreen_cooldown_time = {'itime': 0,
                                         'ftime': 0,
                                         'dtime': 0,
                                         'cooldowntime': 1000}

        # Keyboard and Mouse Inputs{HOLD}
        self.inputs = {'up': False,
                       'down': False,
                       'left': False,
                       'right': False,
                       'lclick': False,
                       'rclick': False,
                       'up2': False,
                       'down2': False,
                       'left2': False,
                       'right2': False,
                       'enter': False,
                       'num1': False,
                       'num2': False,
                       'num3': False,
                       'num4': False,
                       'num5': False,
                       }

    @staticmethod
    def mpos(scaled=False):
        pos = pygame.mouse.get_pos()
        if not scaled:
            return pos
        else:
            return pos[0] // Graphics.DISPLAY_SCALE, pos[1] // Graphics.DISPLAY_SCALE

    def enter_logic(self):
        if not self.game_logic.game_end:
            if self.game_logic.player_choice is not None and not self.cooldown:
                self.game_logic.computer_choice = self.game_logic.rng()
                self.game_logic.rounds += 1
                self.game_logic.winner_logic()
                self.cooldown_type = 'round'
                self.cooldown = True
                self.initial_time = pygame.time.get_ticks()

    def execute_fullscreen(self):
        if not self.fullscreen_cooldown:
            self.fullscreen_cooldown = True
            self.fullscreen_cooldown_time['itime'] = pygame.time.get_ticks()
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                self.window.fill('black')
                pygame.display.flip()
                self.window = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN | pygame.HWSURFACE)
            else:
                self.window.fill('black')
                pygame.display.flip()
                self.window = pygame.display.set_mode(self.size, pygame.HWSURFACE)

    def render_dynamic_surface(self, surface, special_flags=0):
        start = 0
        width = surface.get_width()
        if self.scroll >= 0:
            self.scroll = 0 if self.scroll >= width else self.scroll
        elif self.scroll < 0:
            self.scroll = 0 if self.scroll <= -width else self.scroll
        self.scroll = self.scroll + self.scroll_vx
        first_image_x = start+self.scroll
        second_image_x = start+self.scroll+(width * (1 if self.scroll_vx <= 0 else -1))
        self.window.blit(surface, (first_image_x, 0), special_flags=special_flags)
        self.window.blit(surface, (second_image_x, 0), special_flags=special_flags)

    def render(self, surface, particle_surface=None):
        surface.fill(pygame.Color('black'))
        particle_surface.fill(pygame.Color('black')) if particle_surface is not None else None
        factor = 35
        # pygame.draw.rect(surface, self.color, pygame.Rect((30 + factor, 75, 40, 40)))
        # pygame.draw.rect(surface, self.color2, pygame.Rect((200 + factor, 75, 40, 40)))
        self.particles_m.render()
        self.render_dynamic_surface(import_bg(*self.window.get_size(), (self.screen_bleed_w, self.screen_bleed_h)))
        self.render_dynamic_surface(pygame.transform.scale(self.particle_surface, (self.window.get_width()+self.screen_bleed_w, self.window.get_height()+self.screen_bleed_h)), special_flags=pygame.BLEND_RGBA_ADD)
        # self.window.blit(pygame.transform.scale(self.particle_surface, self.window.get_size()), (self.scroll, 0), special_flags=pygame.BLEND_RGBA_ADD) if particle_surface is not None else None
        blit_asset(self.window, dynamic_texture(texture_load('judgement'), (self.window.get_width(), self.window.get_height()-140*self.screen_factor[1]), 0.75), (86*self.screen_factor[0], 90*self.screen_factor[1]))
        self.vignette.render(self.vignette_surface, self.window)
        self.fade.render(self.window_s, self.window)
        self.window.blit(pygame.transform.scale(surface, self.window.get_size()), (0, 0))

    def update(self):
        # Fullscreen Cooldown
        if self.fullscreen_cooldown_time['itime']:
            self.fullscreen_cooldown_time['ftime'] = pygame.time.get_ticks()
            self.fullscreen_cooldown_time['dtime'] = self.fullscreen_cooldown_time['ftime'] - \
                                                     self.fullscreen_cooldown_time['itime']
            if self.fullscreen_cooldown_time['dtime'] >= self.fullscreen_cooldown_time['cooldowntime']:
                self.fullscreen_cooldown = False
                self.fullscreen_cooldown_time['itime'] = 0
                self.fullscreen_cooldown_time['ftime'] = 0

        if self.game_logic.game_end:
            if not self.initial_time:
                self.initial_time = pygame.time.get_ticks()
                self.cooldown_type = 'end'
                self.cooldown_time = self.cooldown_table[self.cooldown_type]
            self.color = 'white'
            self.color2 = 'white'
        elif not self.cooldown:
            if self.inputs['num1']:
                self.game_logic.player_choice = 1
            elif self.inputs['num2']:
                self.game_logic.player_choice = 2
            elif self.inputs['num3']:
                self.game_logic.player_choice = 3
            elif self.game_logic.level == 2:
                if self.inputs['num4']:
                    self.game_logic.player_choice = 4
                elif self.inputs['num5']:
                    self.game_logic.player_choice = 5

            self.color = self.colordict[self.game_logic.table[self.game_logic.player_choice]]
            self.color2 = 'white'
        else:
            self.color2 = self.colordict[self.game_logic.table[self.game_logic.computer_choice]]

        if self.initial_time:
            self.final_time = pygame.time.get_ticks()
            self.delta_time = self.final_time - self.initial_time
            if self.delta_time >= self.cooldown_time:
                self.cooldown = False
                self.initial_time = 0
                self.final_time = 0
                if self.game_logic.game_end:
                    self.game_logic.game_end = False

        self.screen_factor = [x/y for x, y in zip(self.window.get_size(), self.size)]
        self.scroll_vx = Graphics.SCROLL_VX * self.screen_factor[0]

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    sys.exit()
                # Keyboard and Mouse Inputs:
                # Keyboard Inputs ----->
                if event.type == pygame.KEYDOWN:
                    # Arrow Inputs
                    if event.key == pygame.K_UP:
                        self.inputs['up'] = True
                    if event.key == pygame.K_DOWN:
                        self.inputs['down'] = True
                    if event.key == pygame.K_LEFT:
                        self.inputs['left'] = True
                    if event.key == pygame.K_RIGHT:
                        self.inputs['right'] = True
                    # WASD Inputs
                    if event.key == pygame.K_w:
                        self.inputs['up2'] = True
                    if event.key == pygame.K_s:
                        self.inputs['down2'] = True
                    if event.key == pygame.K_a:
                        self.inputs['left2'] = True
                    if event.key == pygame.K_d:
                        self.inputs['right2'] = True

                    # Fullscreen
                    if event.key == pygame.K_F11:
                        self.execute_fullscreen()
                    # Additional
                    if event.key == pygame.K_RETURN:
                        self.inputs['enter'] = True

                    if event.key == pygame.K_1:
                        self.inputs['num1'] = True
                    if event.key == pygame.K_2:
                        self.inputs['num2'] = True
                    if event.key == pygame.K_3:
                        self.inputs['num3'] = True
                    if event.key == pygame.K_4:
                        self.inputs['num4'] = True
                    if event.key == pygame.K_5:
                        self.inputs['num5'] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.inputs['up'] = False
                    if event.key == pygame.K_DOWN:
                        self.inputs['down'] = False
                    if event.key == pygame.K_LEFT:
                        self.inputs['left'] = False
                    if event.key == pygame.K_RIGHT:
                        self.inputs['right'] = False

                    # WASD Inputs
                    if event.key == pygame.K_w:
                        self.inputs['up2'] = False
                    if event.key == pygame.K_s:
                        self.inputs['down2'] = False
                    if event.key == pygame.K_a:
                        self.inputs['left2'] = False
                    if event.key == pygame.K_d:
                        self.inputs['right2'] = False

                    # Additional Inputs
                    if event.key == pygame.K_RETURN:
                        self.inputs['enter'] = False
                        self.enter_logic()

                    if event.key == pygame.K_1:
                        self.inputs['num1'] = False
                    if event.key == pygame.K_2:
                        self.inputs['num2'] = False
                    if event.key == pygame.K_3:
                        self.inputs['num3'] = False
                    if event.key == pygame.K_4:
                        self.inputs['num4'] = False
                    if event.key == pygame.K_5:
                        self.inputs['num5'] = False

                # Mouse Inputs ----->
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.inputs['lclick'] = True
                    if event.button == 3:
                        self.inputs['rclick'] = True
                    if event.button == 4:
                        pass  # Scroll Up
                    if event.button == 5:
                        pass  # Scroll Down
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.inputs['lclick'] = False
                    if event.button == 3:
                        self.inputs['rclick'] = False

            # Debug:
            pygame.display.set_caption(str(self.clock.get_fps()))
            self.update()
            self.render(self.display, self.particle_surface)
            pygame.display.update()


def main():
    game = Graphics()
    game.run()


if __name__ == '__main__':
    main()
