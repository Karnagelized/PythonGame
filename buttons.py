
import pygame
from pygame.locals import *
from settings import FONT_LINK

class Button:
    def __init__(self, surface:pygame.Surface, button_type:str, color:tuple, pos:pygame.math.Vector2,
                 length:int, height:int, width:int, text:str, text_color:tuple, rounding:int = 0):
        self.screen = surface
        self.button_type = button_type
        self.color = color
        self.position = pygame.math.Vector2(*pos)
        self.length = length
        self.height = height
        self.surface = pygame.Surface((self.length, self.height))
        self.width = width
        self.text = text
        self.text_color = text_color
        self.rounding = rounding

        # Hover
        self.total_position = self.position
        self.total_size = (self.length, self.height)


    def create_button(self):
        surface = self.draw_button()
        surface = self.write_text()
        self.rect = pygame.Rect(self.position.x, self.position.y, self.length, self.height)
        self.total_rect = self.rect

        return surface

    def draw_frame(self):
        pygame.draw.rect(self.screen, (190, 190, 190), (self.position.x, self.position.y, self.length, self.height), 3)

    def draw_button(self):
        self.screen.blit(self.surface, (self.position.x, self.position.y))

        pygame.draw.rect(self.screen, self.color, (self.position.x, self.position.y, self.length, self.height), 0)
        self.draw_frame()

        return self.screen

    def write_text(self):
        font_size = int(self.length // len(self.text))
        myFont = pygame.font.Font(FONT_LINK, 30)
        myText = myFont.render(self.text, 1, self.text_color)

        self.screen.blit(myText, ((self.position.x + self.length / 2) - myText.get_width() / 2,
                                   (self.position.y + self.height / 2) - myText.get_height() / 2))

        return self.screen

    # Change button size from hover
    def hovering(self, mouse):
        self.length, self.height = self.total_size
        self.position = self.total_position

        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0]:
            if self.rect.topleft[1] < mouse[1] < self.rect.bottomright[1]:
                self.position = self.position - pygame.math.Vector2(10, 5)
                self.length += 20
                self.height += 10

    def pressed(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0]:
            if self.rect.topleft[1] < mouse[1] < self.rect.bottomright[1]:
                return True

        return False
