import math
import random
import sys
import time
import pygame
import csv
from datetime import timedelta
from settings import GAME_SETTINGS, WIDTH, HEIGHT, PLANETS_MAP, TEXTURES, TEXTURES_SIZE, FONT_LINK
from keyboard import Keyboard
from support import import_csv, import_folder
from player import Player
from tile import Tile
from camera import CameraGroup
from buttons import Button


class Level():
    def __init__(self):
        # General
        self.game_compl = False
        self.world_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interaction_sprite = pygame.sprite.Group()
        self.background_suond = pygame.mixer.Sound('data/audio/world/background.mp3')
        self.background_suond.set_volume(0.8)

        # Game time
        self.timer_font = pygame.font.Font(FONT_LINK, 24)
        self.time_start = 0
        self.duration = 0

        # Debug
        self.view_hitbox = pygame.sprite.Group()

        # Prolog
        self._prolog_end = False
        self._background = pygame.image.load('data/textures/prolog/end.png')
        self._alpha = 255

        # Game info
        self.INFO = False

        # World
        self.spaceship_img = pygame.image.load('data/textures/prolog/spaceship_512.png')
        self.E_key_img = pygame.image.load('data/textures/ui/E.png')
        self.textures = {
            'grass': import_folder(TEXTURES['grass']),
            'herba': import_folder(TEXTURES['herba']),
            'bush': import_folder(TEXTURES['bush']),
            'water': import_folder(TEXTURES['water']),
            'trees': import_folder(TEXTURES['tree']),
            'useful_tree': import_folder(TEXTURES['useful_tree']),
            'borders': import_folder(TEXTURES['border']),
        }

        # Artefacts
        self.selection_artefact = pygame.mixer.Sound('data/audio/world/selection.mp3')
        self.artefact_list = [
            'chestplate',
            'cup',
            'ring',
            'rune',
            'necklace',
        ]
        self.artefact_img = {
            'necklace': pygame.image.load('data/textures/world/artefact_1.png'),
            'rune': pygame.image.load('data/textures/world/artefact_2.png'),
            'ring': pygame.image.load('data/textures/world/artefact_3.png'),
            'chestplate': pygame.image.load('data/textures/world/artefact_4.png'),
            'cup': pygame.image.load('data/textures/world/artefact_5.png'),
        }

        # Interaction
        self.bush_broken = pygame.mixer.Sound('data/audio/world/bush_brake.mp3')
        self.bush_broken.set_volume(0.2)

        self.spaceship_denied = pygame.mixer.Sound('data/audio/world/access_denied.mp3')

        self.generate_world()

    # Screen emerging after the prolog
    def emerging_screen(self):
        if not self._prolog_end:
            self._alpha -= 2
            self._background.set_alpha(self._alpha)
            self.world_surface.blit(self._background, (0, 0))

            if self._alpha <= 0:
                self._alpha = 0
                self._prolog_end = True
                self.time_start = time.time()
                self.background_suond.play(loops=-1)

    # Screen disappears when game ends
    def disappearing_screen(self):
        if self.game_compl:
            self._alpha += 2
            self._background.set_alpha(self._alpha)
            self.world_surface.blit(self._background, (0, 0))

            if self._alpha >= 254:
                self._alpha = 255

    # Generate world from csv file
    def generate_world(self):
        for _layout in PLANETS_MAP:
            for _y, _line in enumerate(PLANETS_MAP[_layout]):
                for _x, _object in enumerate(_line):
                    if _object not in ['', 0, '||']:
                        if _layout == 'map':
                            if _object == 'g':
                                # Rotate grass on random angle in list [0, 90, 180, 270]
                                _grass = pygame.transform.rotate(self.textures['grass'][0], random.choice([0, 90, 180, 270]))

                                Tile(
                                    [self.visible_sprites],
                                    'grass',
                                    _grass,
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'w':
                                # Water
                                Tile(
                                    [self.visible_sprites],
                                    'water',
                                    self.textures['water'][0],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'bu':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][0],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'bd':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][1],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'bl':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][2],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'br':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][3],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )

                            elif _object == 'b_u_l':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][4],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )

                            elif _object == 'b_b_l':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][5],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b_u_r':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][6],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b_b_r':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][7],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b_ul':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][8],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b_ur':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][9],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b_bl':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][10],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b_br':
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'border',
                                    self.textures['borders'][11],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                        elif _layout == 'plants':
                            if _object == 't':
                                # Common tree
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    'tree',
                                    random.choice(self.textures['trees']),
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y),
                                )
                            elif _object == 'UT':
                                # Tree with apple
                                _count_apple = random.randint(1, 3)

                                if _count_apple == 1:
                                    _tree_texture = self.textures['useful_tree'][1]
                                elif _count_apple == 2:
                                    _tree_texture = self.textures['useful_tree'][2]
                                elif _count_apple == 3:
                                    _tree_texture = self.textures['useful_tree'][3]

                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites, self.interaction_sprite, self.view_hitbox],
                                    'useful_tree',
                                    _tree_texture,
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y),
                                    {'apples': _count_apple, 'images': self.textures['useful_tree']},
                                )
                            elif _object == 'h':
                                # Herba
                                Tile(
                                    [self.visible_sprites],
                                    'herba',
                                    random.choice(self.textures['herba']),
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'b':
                                # Bush
                                Tile(
                                    [self.visible_sprites, self.interaction_sprite, self.view_hitbox],
                                    'bush',
                                    self.textures['bush'][0],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y),
                                    {'barbed': True}
                                )
                        elif _layout == 'entity':
                            if _object == 'p':
                                # Player
                                self.player = Player(
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                        elif _layout == 'objects':
                            if _object == 'sh':
                                # Spaceship
                                Tile(
                                    [self.visible_sprites, self.obstacle_sprites, self.interaction_sprite, self.view_hitbox],
                                    'spaceship',
                                    self.spaceship_img,
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y)
                                )
                            elif _object == 'A':
                                # Artefact
                                artefact_type = random.choice(self.artefact_list)
                                self.artefact_list.remove(artefact_type)

                                Tile(
                                    [self.visible_sprites, self.interaction_sprite, self.view_hitbox],
                                    'artefact',
                                    self.artefact_img[artefact_type],
                                    pygame.math.Vector2(_x * TEXTURES_SIZE.x, _y * TEXTURES_SIZE.y),
                                    {'artefact_type': artefact_type}
                                )


    # Elapsed time in game
    def view_game_time(self):
        if self._prolog_end and not self.game_compl:
            self.duration = int(time.time() - self.time_start)

        game_timer = self.timer_font.render(f'Time: {timedelta(seconds=self.duration)}', 0, (255, 255, 255))
        self.world_surface.blit(game_timer, (10, 10))


    # Collect apple from apple tree to add hunger or health
    def interaction(self):
        for sprite in self.interaction_sprite:
            if sprite.is_interaction:
                if sprite.interaction.colliderect(self.player):
                    keys = pygame.key.get_pressed()

                    # Draw E key to interact with object
                    # Ignore someone objects
                    if sprite.sprite_type not in ['bush']:
                        rc = self.E_key_img.get_rect(
                            left=sprite.hitbox.left - self.visible_sprites.offset.x + sprite.image_size[0] // 2 - 16,
                            top=sprite.hitbox.top - self.visible_sprites.offset.y - 40,
                        )
                        self.world_surface.blit(self.E_key_img, rc)

                    if sprite.sprite_type == 'useful_tree':
                        if sprite.data['apples'] > 0:
                            # Collect apple from tree
                            if keys[pygame.K_e] and Keyboard.key_E:
                                self.player.eat_food(sprite)
                    elif sprite.sprite_type == 'bush':
                        if sprite.data['barbed']:
                            # Bush update
                            random.choice(self.player.damage_sound).play()
                            self.bush_broken.play()
                            sprite.image = self.textures['bush'][1]
                            sprite.data['barbed'] = False

                            # Player damage
                            self.player.stats['health'] -= 1
                            self.player.player_death()

                            # Statistic
                            self.player.statistic['broken bushes'] += 1
                            self.player.statistic['hearts lost'] += 1
                    elif sprite.sprite_type == 'artefact':
                        if keys[pygame.K_e] and Keyboard.key_E:
                            self.selection_artefact.play()

                            # Add artefact in player inventory
                            item = sprite.data['artefact_type']
                            self.player.inventory['items'][item]['collected'] = True
                            sprite.kill()
                    elif sprite.sprite_type == 'spaceship':
                        if keys[pygame.K_e] and Keyboard.key_E:
                            if all([item_collect[1]['collected'] for item_collect in self.player.inventory['items'].items()]):
                                self.game_compl = True
                            else:
                                self.spaceship_denied.stop()
                                self.spaceship_denied.play()

    # DEBUG
    def draw_hitbox(self):
        """
        Use self.view_hitbox in sprite group, for view hitbox on sprite
        """
        if GAME_SETTINGS.DEBUG:
            for sprite in self.view_hitbox.sprites():
                sprite: Tile()
                hitbox_rect = pygame.rect.Rect(
                    sprite.hitbox.left - self.visible_sprites.offset.x - 25,
                    sprite.hitbox.top - self.visible_sprites.offset.y - 25,
                    sprite.hitbox.width + 50,
                    sprite.hitbox.height + 50
                )

                pygame.draw.rect(self.world_surface, (255, 255, 255), hitbox_rect, 2)

    def run(self):
        # Draw all object's
        self.world_surface.fill('#b6c4ff')
        self.visible_sprites.custom_draw(self.player)
        self.view_game_time()
        self.draw_hitbox()

        # Update Player
        self.player.update(self._prolog_end, self.game_compl)
        self.interaction()
        Keyboard.update()

        # Prolog
        self.emerging_screen()

        # Ending
        self.disappearing_screen()
