
import pygame
from support import import_csv


# User game settings
class Settings():
    def __init__(self):
        # Use for more info about game
        self.GAME_INFO = False
        self.DEBUG = False

GAME_SETTINGS = Settings()


### GENERAL SETTINGS ###
# Game name
GAME_NAME = 'Uncharted Realm'

# Size's of Game screen
SIZE = WIDTH, HEIGHT = 1920, 1080

# Using FPS in game
FPS = 60

# Font
FONT_LINK = 'font/CustomFont.ttf'


### Map ###
# Generate
PLANETS_MAP = {
    'map': import_csv('data/map/map.csv'),
    'plants': import_csv('data/map/plants.csv'),
    'objects': import_csv('data/map/objects.csv'),
    'entity': import_csv('data/map/entity.csv'),
}

# Textures
TEXTURES_SIZE = pygame.math.Vector2(128, 128)

TEXTURES = {
    'grass': [
            'data/textures/world/grass.png',
    ],
    'water': [
        'data/textures/world/water.png',
    ],
    'herba': [
        'data/textures/world/grass_1.png',
        'data/textures/world/grass_2.png',
        'data/textures/world/grass_3.png',
    ],
    'bush': [
        'data/textures/world/bush_1.png',
        'data/textures/world/bush_2.png',
    ],
    'useful_tree': [
        'data/textures/world/tree_1.png',
        'data/textures/world/apple_tree_1.png',
        'data/textures/world/apple_tree_2.png',
        'data/textures/world/apple_tree_3.png',
    ],
    'tree': [
            'data/textures/world/tree_2.png',
            'data/textures/world/tree_3.png',
            'data/textures/world/tree_4.png',
            'data/textures/world/tree_5.png',
            'data/textures/world/tree_6.png',
            'data/textures/world/tree_7.png',
    ],
    'border': [
        'data/textures/world/border_up.png',
        'data/textures/world/border_bottom.png',
        'data/textures/world/border_left.png',
        'data/textures/world/border_right.png',

        'data/textures/world/border_up_left.png',
        'data/textures/world/border_bt_left.png',
        'data/textures/world/border_up_right.png',
        'data/textures/world/border_bt_right.png',

        'data/textures/world/border_ul.png',
        'data/textures/world/border_ur.png',
        'data/textures/world/border_bl.png',
        'data/textures/world/border_br.png',
    ],
}


### Player ###
WALK_TIMER = 18
WALK_AUDIO = [
    'data/audio/player/walk_1.wav',
    'data/audio/player/walk_2.wav',
    'data/audio/player/walk_3.wav',
    'data/audio/player/walk_4.wav',
    'data/audio/player/walk_5.wav',
    'data/audio/player/walk_6.wav',
]

PLAYER_ANIMATION = {
    'IDLE': {
        'DOWN': 'data/textures/player/idle/idle_down',
        'LEFT': 'data/textures/player/idle/idle_left',
        'RIGHT': 'data/textures/player/idle/idle_right',
        'UP': 'data/textures/player/idle/idle_up',
    },
    'WALK': {
        'DOWN': 'data/textures/player/walk/walk_down',
        'LEFT': 'data/textures/player/walk/walk_left',
        'RIGHT': 'data/textures/player/walk/walk_right',
        'UP': 'data/textures/player/walk/walk_up',
    },
}

### Sound
PLAYER_SOUND = {
    'refusal_eat': [
        'data/audio/player/no_1.ogg',
        'data/audio/player/no_2.ogg',
        'data/audio/player/no_3.ogg',
        'data/audio/player/no_4.ogg',
    ],
    'auch': [
        'data/audio/player/auch_1.ogg',
        'data/audio/player/auch_2.ogg',
    ],
}
