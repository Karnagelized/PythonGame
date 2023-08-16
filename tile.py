
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, group:pygame.sprite.Sprite, sprite_type:str, image:pygame.image, position:pygame.math.Vector2, data:dict={}):
        super().__init__(group)
        # General
        self.sprite_type = sprite_type
        self.image = image
        self.image_size = self.image.get_size()
        self.rect = self.image.get_rect(center=(position.x, position.y))
        self.hitbox = self.rect
        self.data = data

        # Для взаимодействий
        if sprite_type in ['useful_tree', 'spaceship']:
            self.is_interaction = True
            self.interaction = self.image.get_rect(center=(position.x - 25, position.y - 25))
            self.interaction.width += 50
            self.interaction.height += 50
        elif sprite_type in ['bush', 'artefact']:
            self.is_interaction = True
            self.interaction = self.image.get_rect(center=(position.x, position.y))