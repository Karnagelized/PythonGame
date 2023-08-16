
import pygame
import random
import os
import copy
from settings import WIDTH, HEIGHT, PLAYER_ANIMATION, FONT_LINK, WALK_AUDIO, WALK_TIMER, PLAYER_SOUND
from ui import UI
from entity import Entity
from keyboard import Keyboard
from support import import_sounds


class Player(Entity):
    def __init__(self, group:pygame.sprite.Sprite, obstacle_sprites:pygame.sprite.Sprite, position:pygame.math.Vector2):
        super().__init__(group)
        # General
        self.image = pygame.image.load('data/textures/player/idle/idle_down/idle_down.png')
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect
        self.ui = UI()
        self.statistic = {
            'passed pixels': 0,
            'eaten apples': 0,
            'broken bushes': 0,
            'hearts lost': 0,
        }

        # Movement
        self.obstacle_sprites = obstacle_sprites

        # Textures
        self.load_animation()
        self.status = 'DOWN'
        self.fettle = 'IDLE'
        self.walk_sound_timer = 0

        ### Sound
        self.load_walk_sounds()
        self.health_time = 0
        self.hunger_time = 0
        self.energy_time = 0
        self.energy_recover_time = 0

        # Hunger
        self.hungry_sound = pygame.mixer.Sound('data/audio/player/hungry.ogg')
        self.hungry_sound.set_volume(0.8)

        # Eat
        self.eat_sound = pygame.mixer.Sound('data/audio/player/eat.mp3')
        self.eat_sound.set_volume(0.5)

        # Refusal to eat
        self.refusal_eat_sound = import_sounds(PLAYER_SOUND['refusal_eat'])

        # Damage
        self.damage_sound = import_sounds(PLAYER_SOUND['auch'])

        # Loss of health
        self.loss_health_sound = pygame.mixer.Sound('data/audio/player/loss_health.mp3')
        self.loss_health_sound.set_volume(0.8)

        # Die
        self.die_sound = pygame.mixer.Sound('data/audio/player/game_over.wav')
        self.die_sound.set_volume(0.6)

        # Characteristics
        self.is_die = False

        self.stats = {
            'speed': 5,
            'health': 5,
            'hungry': 5,
            'energy': 5,
        }
        self.speed = self.stats['speed']

        self.inventory = {
            'active': False,
            'items': {
                'chestplate': {
                    'collected': False,
                    'image': [
                        pygame.image.load('data/textures/UI/artefact_1.png'),
                        pygame.image.load('data/textures/UI/artefact_2.png'),
                    ],
                },
                'cup': {
                    'collected': False,
                    'image': [
                        pygame.image.load('data/textures/UI/artefact_3.png'),
                        pygame.image.load('data/textures/UI/artefact_4.png'),
                    ],
                },
                'ring': {
                    'collected': False,
                    'image': [
                        pygame.image.load('data/textures/UI/artefact_5.png'),
                        pygame.image.load('data/textures/UI/artefact_6.png'),
                    ],
                },
                'rune': {
                    'collected': False,
                    'image': [
                        pygame.image.load('data/textures/UI/artefact_7.png'),
                        pygame.image.load('data/textures/UI/artefact_8.png'),
                    ],
                },
                'necklace': {
                    'collected': False,
                    'image': [
                        pygame.image.load('data/textures/UI/artefact_9.png'),
                        pygame.image.load('data/textures/UI/artefact_10.png'),
                    ],
                },
            }
        }

    def play_refusal_eat_sound(self):
        random.choice(self.refusal_eat_sound).play()

    def load_walk_sounds(self):
        self.walk_sounds = []

        for sound in WALK_AUDIO:
            mixer = pygame.mixer.Sound(sound)
            mixer.set_volume(0.1)
            self.walk_sounds.append(mixer)

    def load_animation(self):
        self.animations = copy.deepcopy(PLAYER_ANIMATION)

        for key in PLAYER_ANIMATION:
            for item in PLAYER_ANIMATION[key]:
                ls_item = []
                _dir = os.listdir(PLAYER_ANIMATION[key][item])

                for image in _dir:
                    ls_item.append(pygame.image.load(f'{PLAYER_ANIMATION[key][item]}/{image}'))

                self.animations[key][item] = ls_item

    def input(self):
        keys = pygame.key.get_pressed()

        # Player horizontal step's
        if keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'DOWN'
            self.fettle = 'WALK'
        elif keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'UP'
            self.fettle = 'WALK'
        else:
            self.direction.y = 0

        # Player vertical step's
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'LEFT'
            self.fettle = 'WALK'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'RIGHT'
            self.fettle = 'WALK'
        else:
            self.direction.x = 0

        # Default walk
        self.speed = self.stats['speed']
        self.animation_speed = 0.1

        # Run
        if self.stats['energy'] > 0:
            if keys[pygame.K_LSHIFT]:
                self.speed = 7
                self.animation_speed = 0.15

        # Play walk sound
        self.walk_sound()

    # Animation player on screen
    def animate(self):
        animation = self.animations[self.fettle][self.status]

        self.texture_index += self.animation_speed
        if self.texture_index >= len(animation):
            self.texture_index = 0

        self.image = animation[int(self.texture_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        self.fettle = 'IDLE'

    # Sound when user walk
    def walk_sound(self):
        if self.fettle == 'WALK':
            self.walk_sound_timer += 1

            if self.walk_sound_timer >= 18:
                self.walk_sound_timer = 0
                random.choice(self.walk_sounds).play()

    def hunger_update(self):
        self.hunger_time += 1

        # Hunger
        if self.hunger_time >= 1400:
            self.hunger_time = 0

            if self.stats['hungry'] > 0:
                self.stats['hungry'] -= 1

                if self.stats['hungry'] < 3:
                    self.hungry_sound.play()

    def health_update(self):
        if self.stats['hungry'] == 0:
            self.health_time += 1

            if self.health_time >= 1000:
                self.health_time = 0
                self.stats['health'] -= 1
                self.statistic['hearts lost'] += 1

                if self.stats['health'] > 0:
                    self.loss_health_sound.play()

                self.player_death()

    def energy_update(self):
        if not Keyboard.key_LSHIFT:
            self.energy_time += 1

            if self.energy_time >= 80:
                self.energy_time = 0
                self.stats['energy'] -= 1

        # Recovery
        if Keyboard.key_LSHIFT:
            if self.stats['energy'] < 5:
                self.energy_recover_time += 1

                if self.energy_recover_time >= 150:
                    self.energy_recover_time = 0
                    self.stats['energy'] += 1

    def eat_food(self, sprite:pygame.sprite.Sprite):
        if self.stats['hungry'] < 5 or self.stats['health'] < 5:
            self.statistic['eaten apples'] += 1
            self.eat_sound.play()
            self.hunger_time = 0
            self.health_time = 0

            # Add health if hungry is empty or add hungry if health is full and hungry is empty
            if self.stats['health'] < 5:
                self.stats['health'] += 1
            else:
                self.stats['hungry'] += 1

            sprite.data['apples'] -= 1
            sprite.image = sprite.data['images'][sprite.data['apples']]

            # Delete interation flag if apple == 0
            if sprite.data['apples'] == 0:
                sprite.is_interaction = False
        else:
            self.play_refusal_eat_sound()

    def stats_update(self):
        self.hunger_update()
        self.health_update()
        self.energy_update()


    # END game
    def player_death(self):
        if self.stats['health'] <= 0:
            self.die_sound.play()
            self.is_die = True


    def update(self, prolog_end:bool, game_compl:bool):
        # Check end of prolog
        if prolog_end and not game_compl:
            self.input()
            self.animate()
            self.move()
            self.stats_update()

        self.ui.display(self.stats, self.inventory)
