
import pygame

class Keyboard:
    key_E = True
    key_LSHIFT = True
    key_TAB = True

    @classmethod
    def update(cls):
        keys = pygame.key.get_pressed()
        cls.key_E = True
        cls.key_LSHIFT = True
        cls.key_TAB = True

        if keys[pygame.K_e]:
            cls.key_E = False

        if keys[pygame.K_LSHIFT]:
            cls.key_LSHIFT = False

        if keys[pygame.K_TAB]:
            cls.key_TAB = False
