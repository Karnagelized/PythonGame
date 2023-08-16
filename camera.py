
import pygame
from settings import WIDTH, HEIGHT


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		# Camera offset
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# General
		self.camera_speed = 5
		self.camera_borders = {
            'left': 100,
            'right': 100,
            'top': 50,
            'bottom': 50
        }

		self.camera_rect = pygame.Rect(
			self.camera_borders['left'],
			self.camera_borders['top'],
			WIDTH  - (self.camera_borders['left'] + self.camera_borders['right']),
			HEIGHT  - (self.camera_borders['top'] + self.camera_borders['bottom']),
		)

	# Drawing objects on user screen
	def custom_draw(self, player):
		# Camera offsets by player
		self.center_target_camera(player)

		# Draw all visible sprites
		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)

	def center_target_camera(self, target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h