
import pygame
import time
from datetime import timedelta
from settings import HEIGHT, FONT_LINK
from keyboard import Keyboard

class UI():
    def __init__(self):
        # General
        self.surface = pygame.display.get_surface()

        self.hunger_img = pygame.image.load('data/textures/UI/hunger.png')
        self.heart_img = pygame.image.load('data/textures/UI/heart.png')
        self.energy_img = pygame.image.load('data/textures/UI/energy.png')
        self.player_ui = pygame.image.load('data/textures/UI/player_ui.png')
        self.player_bag = pygame.image.load('data/textures/UI/bag.png')

    def view_inventory(self, player_inventory:dict):
        keys = pygame.key.get_pressed()

        # Active/Inactive player inventory
        if keys[pygame.K_TAB] and Keyboard.key_TAB:
            player_inventory['active'] = not player_inventory['active']

        # Draw inventory
        if player_inventory['active']:
            for _, item in enumerate(player_inventory['items'].items()):
                self.surface.blit(item[1]['image'][item[1]['collected']], (10, HEIGHT - 240 - 120 * _))
        else:
            self.surface.blit(self.player_bag, (10, HEIGHT - 240))

    # Draw on screen UI
    def display(self, player_stats:dict, player_inventory:dict):
        # Player icon
        self.surface.blit(self.player_ui, (10, HEIGHT - 120))

        # Count health
        for _ in range(player_stats['health']):
            self.surface.blit(self.heart_img, (125 + 32 * _, HEIGHT - 115))

        # Count hungry
        for _ in range(player_stats['hungry']):
            self.surface.blit(self.hunger_img, (125 + 32 * _, HEIGHT - 85))

        # Count hungry
        for _ in range(player_stats['energy']):
            self.surface.blit(self.energy_img, (125 + 32 * _, HEIGHT - 45))

        # Inventory
        self.view_inventory(player_inventory)