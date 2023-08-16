import datetime
import os
import random
import sys
import time

import pygame
from settings import WIDTH, HEIGHT, FONT_LINK
from support import import_folder


# Text on screen
class Annotations:
    def __init__(self, surface:pygame.Surface):
        # General
        self.surface = surface
        self.finished = False
        self.timer = 0
        self.direction = 1
        self.position = (0, 0)
        self.load_reflections()

        # Music
        self.music_on = True
        self.music = pygame.mixer.Sound('data/audio/prolog/background.mp3')
        self.music.set_volume(0.2)

    def load_reflections(self):
        self.reflections = [
            {
                'img': pygame.image.load('data/textures/prolog/text/introduction.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/sora_1.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/sora_2.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/sora_3.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/sora_4.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/sora_5.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/brain_1.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/text/brain_2.png'),
                'alpha': 0,
            },
            {
                'img': pygame.image.load('data/textures/prolog/end.png'),
                'alpha': 0,
            }
        ]

        for reflection in self.reflections:
            reflection['img'].set_alpha(reflection['alpha'])

    def update(self):
        self.timer += 1

        if 400 <= self.timer <= 910:    # Introduction
            if self.reflections[0]['alpha'] >= 255:
                self.direction = -1

            self.reflections[0]['alpha'] += self.direction
            self.reflections[0]['img'].set_alpha(self.reflections[0]['alpha'])

            self.surface.blit(self.reflections[0]['img'], self.position)

            if self.direction < 0 and self.reflections[0]['alpha'] < 0:
                self.direction = 1
        elif 910 < self.timer <= 1420:  # sora_1
            if self.music_on:
                self.music_on = False
                self.music.play()

            if self.reflections[1]['alpha'] >= 255:
                self.direction = -1

            self.reflections[1]['alpha'] += self.direction
            self.reflections[1]['img'].set_alpha(self.reflections[1]['alpha'])

            self.surface.blit(self.reflections[1]['img'], self.position)

            if self.direction < 0 and self.reflections[1]['alpha'] < 0:
                self.direction = 1
        elif 1420 < self.timer <= 1930: # sora_2
            if self.reflections[2]['alpha'] >= 255:
                self.direction = -1

            self.reflections[2]['alpha'] += self.direction
            self.reflections[2]['img'].set_alpha(self.reflections[2]['alpha'])

            self.surface.blit(self.reflections[2]['img'], self.position)

            if self.direction < 0 and self.reflections[2]['alpha'] < 0:
                self.direction = 1
        elif 1930 < self.timer <= 2440: # sora_3
            if self.reflections[3]['alpha'] >= 255:
                self.direction = -1

            self.reflections[3]['alpha'] += self.direction
            self.reflections[3]['img'].set_alpha(self.reflections[3]['alpha'])

            self.surface.blit(self.reflections[3]['img'], self.position)

            if self.direction < 0 and self.reflections[3]['alpha'] < 0:
                self.direction = 1
        elif 2440 < self.timer <= 2950: # sora_4
            if self.reflections[4]['alpha'] >= 255:
                self.direction = -1

            self.reflections[4]['alpha'] += self.direction
            self.reflections[4]['img'].set_alpha(self.reflections[4]['alpha'])

            self.surface.blit(self.reflections[4]['img'], self.position)

            if self.direction < 0 and self.reflections[4]['alpha'] < 0:
                self.direction = 1
        elif 2950 < self.timer <= 3460: # sora_5
            if self.reflections[5]['alpha'] >= 255:
                self.direction = -1

            self.reflections[5]['alpha'] += self.direction
            self.reflections[5]['img'].set_alpha(self.reflections[5]['alpha'])

            self.surface.blit(self.reflections[5]['img'], self.position)

            if self.direction < 0 and self.reflections[5]['alpha'] < 0:
                self.direction = 1
        elif 3460 < self.timer <= 3970: # brain_1
            if self.reflections[6]['alpha'] >= 255:
                self.direction = -1

            self.reflections[6]['alpha'] += self.direction
            self.reflections[6]['img'].set_alpha(self.reflections[6]['alpha'])

            self.surface.blit(self.reflections[6]['img'], self.position)

            if self.direction < 0 and self.reflections[6]['alpha'] < 0:
                self.direction = 1
        elif 3970 < self.timer <= 4480: # brain_2
            if self.reflections[7]['alpha'] >= 255:
                self.direction = -1

            self.reflections[7]['alpha'] += self.direction
            self.reflections[7]['img'].set_alpha(self.reflections[7]['alpha'])

            self.surface.blit(self.reflections[7]['img'], self.position)

            if self.direction < 0 and self.reflections[7]['alpha'] < 0:
                self.direction = 1
        elif self.timer > 4480:
            self.reflections[8]['alpha'] += 1
            self.reflections[8]['img'].set_alpha(self.reflections[8]['alpha'])

            self.surface.blit(self.reflections[8]['img'], self.position)

            if self.reflections[8]['alpha'] == 255:
                self.finished = True


class Planets:
    def __init__(self, surface:pygame.Surface):
        # General
        self.surface = surface
        self.planet_size = (128, 128)
        self.speed = pygame.math.Vector2(0, 1)
        self.find_planet = False
        self.load_unsuitable_planets()

    def load_unsuitable_planets(self):
        self.unsuitable_planets = [
            {
                'img': pygame.image.load('data/textures/prolog/planets/Ice.png'),
                'position': pygame.math.Vector2(350, -140),
                'size': (192, 192)
            },
            {
                'img': pygame.image.load('data/textures/prolog/planets/Lava.png'),
                'position': pygame.math.Vector2(150, 700),
                'size': (256, 256)
            },
            {
                'img': pygame.image.load('data/textures/prolog/planets/Baren.png'),
                'position': pygame.math.Vector2(1200, 700),
                'size': (192, 192)
            },
            {
                'img': pygame.image.load('data/textures/prolog/planets/Green.png'),
                'position': pygame.math.Vector2(1500, -140),
                'size': (256, 256)
            },
            {
                'img': pygame.image.load('data/textures/prolog/planets/Aqua.png'),
                'position': pygame.math.Vector2(1700, 400),
                'size': (128, 128)
            },
            {
                'img': pygame.image.load('data/textures/prolog/planets/Blue.png'),
                'position': pygame.math.Vector2(600, 200),
                'size': (128, 128)
            },
            {
                'img': pygame.image.load('data/textures/prolog/planets/Splash.png'),
                'position': pygame.math.Vector2(-64, -10),
                'size': (128, 128)
            },
            # Terrain
            {
                'img': pygame.image.load('data/textures/prolog/planets/Terran.png'),
                'flag': True,
                'position': pygame.math.Vector2(WIDTH // 2 - 64, -1900),
                'size': (128, 128)
            },
        ]

    def update(self, timer:int):
        for planet in self.unsuitable_planets:
            if not self.find_planet:
                # Moving
                planet['position'] += self.speed

                # Move up to reset moving in space
                if planet['position'].y > HEIGHT + planet['size'][1]:
                    planet['position'] = (planet['position'].x, -planet['size'][1])

                # Find Terra
                if 'flag' in planet:
                    if planet['position'].y > HEIGHT // 4:
                        self.find_planet = planet['flag']

            self.surface.blit(planet['img'], planet['position'])


class Spaceship():
    def __init__(self, surface:pygame.Surface):
        # General
        self.surface = surface

        # Whole
        self.is_visible = True
        self.spaceship_textures = import_folder('data/textures/prolog/spaceship')
        self.spaceship = self.spaceship_textures[0]
        self.static_spaceship = pygame.image.load('data/textures/prolog/spaceship_256.png')
        self.animate_speed = 0.15
        self.texture_ind = 0
        self.size = self.spaceship.get_size()
        self.rect = self.spaceship.get_rect(x=WIDTH // 2 - self.size[0] // 2, y=HEIGHT + 100)

    def animate(self, find_planet:bool, timer:int):
        if find_planet and timer < 4480:
            self.spaceship = self.static_spaceship
        else:
            self.texture_ind += self.animate_speed

            if self.texture_ind >= len(self.spaceship_textures):
                self.texture_ind = 0

            self.spaceship = self.spaceship_textures[int(self.texture_ind)]


    def update(self, find_planet:bool, timer:int):
        self.animate(find_planet, timer)

        if not find_planet:
            if self.rect.y > HEIGHT - self.rect.height - 100:
                self.rect.y -= 1
        else:
            if timer > 4480:
                if self.rect.y > HEIGHT // 2 - 300:
                    self.rect.y -= 2
                else:
                    self.is_visible = not self.is_visible

        if self.is_visible:
            self.surface.blit(self.spaceship, self.rect)


class Space:
    def __init__(self, surface:pygame.Surface):
        # General
        self.surface = surface
        self.background_space = pygame.image.load('data/textures/prolog/space.png').convert()
        self.background_size = self.background_space.get_size()
        self.rect_space_one = self.background_space.get_rect(y=HEIGHT - self.background_size[1])
        self.rect_space_two = self.background_space.get_rect(y=HEIGHT - 2 * self.background_size[1] - 1)

    def update(self, find_planet:bool):
        self.surface.blit(self.background_space, self.rect_space_one)
        self.surface.blit(self.background_space, self.rect_space_two)

        # Moving
        if not find_planet:
            self.rect_space_one.y += 1
            self.rect_space_two.y += 1

            if self.rect_space_one.y > HEIGHT:
                self.rect_space_one.y = HEIGHT - 2 * self.background_size[1]

            if self.rect_space_two.y > HEIGHT:
                self.rect_space_two.y = HEIGHT - 2 * self.background_size[1] - 1


class Prolog():
    def __init__(self):
        # General
        self.surface = pygame.display.get_surface()
        self.annotation = Annotations(self.surface)
        self.space = Space(self.surface)
        self.planets = Planets(self.surface)
        self.spaceship = Spaceship(self.surface)

    def view_skip(self):
        _myFont = pygame.font.Font(FONT_LINK, 22)
        _prolog = _myFont.render('Press Enter to skip', 0, (255, 255, 255))
        _size = _prolog.get_size()

        self.surface.blit(_prolog, (WIDTH - _size[0] - 20, HEIGHT - _size[1] - 10))

    # Update
    def run(self):
        self.space.update(self.planets.find_planet)
        self.planets.update(self.annotation.timer)
        self.spaceship.update(self.planets.find_planet, self.annotation.timer)
        self.annotation.update()
        self.view_skip()


class Ending():
    def __init__(self):
        self.surface = pygame.display.get_surface()

        # Main text
        self._font = pygame.font.Font(FONT_LINK, 40)
        self._end = self._font.render('Thanks for playing!', 0, (255, 255, 255))
        self.text_pos = (WIDTH // 2 - self._end.get_width() // 2, HEIGHT // 6 - self._end.get_height())


        # Restart text
        self.restart_font = pygame.font.Font(FONT_LINK, 20)
        self.restart_game = self.restart_font.render('Press R to restart', 0, (255, 255, 255))
        self.restart_pos = (WIDTH - self.restart_game.get_width() - 20, HEIGHT - self.restart_game.get_height() - 20)

        # Statistic
        self.statistic_font = pygame.font.Font(FONT_LINK, 26)

    def run(self, statistic:dict, game_time:time.struct_time):
        # Main text
        self.surface.blit(self._end, self.text_pos)

        # Restart game
        self.surface.blit(self.restart_game, self.restart_pos)

        # Statistic
        for _, item in enumerate(statistic.items()):
            statistic_text = self.statistic_font.render(f'{item[0].capitalize()}: {item[1]}', 0, (255, 255, 255))
            statistic_pos = (WIDTH // 2 - statistic_text.get_width() // 2, HEIGHT // 3 + statistic_text.get_height() * 3 * _)
            self.surface.blit(statistic_text, statistic_pos)

        # Time
        total_time = self.statistic_font.render(f'Playing time: {datetime.timedelta(seconds=game_time)}', 0, (255, 255, 255))
        time_pos = (WIDTH // 2 - total_time.get_width() // 2, HEIGHT // 3 + statistic_text.get_height() * 4 * len(statistic))
        self.surface.blit(total_time, time_pos)