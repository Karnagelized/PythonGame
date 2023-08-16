
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups:[pygame.sprite.Sprite]):
        super().__init__(groups)
        # General
        self.texture_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.math.Vector2()

    def move(self):
        self.hitbox.x +=  self.direction.x * self.speed
        self.statistic['passed pixels'] += int(abs(self.direction.x * self.speed))
        self.check_obstacle('horizontal')
        self.hitbox.y +=  self.direction.y * self.speed
        self.statistic['passed pixels'] += int(abs(self.direction.y * self.speed))
        self.check_obstacle('vertical')
        self.rect.center = self.hitbox.center

    def check_obstacle(self, direction:str):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
