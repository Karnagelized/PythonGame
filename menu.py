
import pygame
import webbrowser
from settings import SIZE, GAME_NAME, FONT_LINK
from buttons import Button


# Menu annotations
class Annotation():
    def __init__(self, num:int, path:str, link:str):
        # General
        self.path = path
        self.link = link
        self.image = pygame.image.load(self.path)
        self.size = self.image.get_size()
        self.margin = 50
        self.padding = 25
        self.rect = self.image.get_rect(
            x=SIZE[0] - 5 - num * self.margin - (num - 1) * self.padding,
            y=SIZE[1] - 5 - self.size[1],
        )

    def create_link(self):
        _surf = pygame.display.get_surface()
        _surf.blit(self.image, (self.rect.x, self.rect.y))

    def hovering(self, position:pygame.mouse):
        if self.rect.x <= position[0] <= self.rect.x + self.rect.width:
            if self.rect.y <= position[1] <= self.rect.y + self.rect.height:
                pygame.draw.line(pygame.display.get_surface(), (255, 255, 255, 10),
                                 (self.rect.x, self.rect.y + self.rect.height),
                                 (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
                                 width=2,
                                 )

    def pressed(self, position:pygame.mouse):
        if self.rect.x <= position[0] <= self.rect.x + self.rect.width:
            if self.rect.y <= position[1] <= self.rect.y + self.rect.height:
                webbrowser.open(self.link)


# Main menu
class Menu():
    def __init__(self, screen:pygame.display, center_screen:pygame.math.Vector2, play_sound:bool=True):
        # General
        self.screen = screen
        self.center_screen = center_screen
        self.butt_count = 2
        self.width = 180
        self.height = 60
        self.margin = 50
        self.beginning_position = (SIZE[1] - self.butt_count * (self.height + 2 * self.margin) + 2 * self.margin) // 2

        # Background
        self.background = pygame.image.load('data/textures/menu/background.jpg')

        # Sound
        self.sound_active = False
        self.sound = pygame.mixer.Sound('data/audio/menu/background.mp3')
        self.sound.set_volume(1)

        # Annotations
        self.GIT = Annotation(
            num = 3,
            link = 'https://github.com/Karnagelized',
            path='data/textures/menu/git.png',
        )
        self.VK = Annotation(
            num = 2,
            link = 'https://vk.com/id318377923',
            path='data/textures/menu/vk.png',
        )
        self.TG = Annotation(
            num = 1,
            link = 'https://t.me/masikantonov',
            path='data/textures/menu/tg.png',
        )

        # Init Buttons
        if play_sound:
            self.switch_sound()
        self.init_buttons()
        self.create_menu_button()
        self.create_pause_button()
        self.create_restart_button()

    def switch_sound(self):
        self.sound_active = not self.sound_active

        if self.sound_active:
            self.sound.play(loops=-1)
        else:
            pygame.mixer.stop()

    def view_restart_text(self):
        _myFont = pygame.font.Font(FONT_LINK, 60)
        _myText = _myFont.render(f'You died!', 1, (255, 255, 255))

        self.screen.blit(_myText, (self.center_screen.x - _myText.get_width() // 2, 150))

    def view_pause_text(self):
        _myFont = pygame.font.Font(FONT_LINK, 60)
        _myText = _myFont.render(f'Paused', 1, (255, 255, 255))

        self.screen.blit(_myText, (self.center_screen.x - _myText.get_width() // 2, 150))

    def view_game_name(self):
        _myFont = pygame.font.Font(FONT_LINK, 60)
        _myText = _myFont.render(f'{GAME_NAME}', 1, (255, 255, 255))

        self.screen.blit(_myText, (self.center_screen.x - _myText.get_width() // 2, 150))

    def view_creator(self):
        _myFont = pygame.font.Font(FONT_LINK, 22)
        _creator = _myFont.render('Created by Karnagelized', 0, (255, 255, 255))

        self.screen.blit(_creator, (10, SIZE[1] - 30))

    def init_buttons(self):
        self.MENU = Button(
            self.screen,
            'restart_button',
            (148, 158, 230),
            (self.center_screen.x - self.width // 2, self.get_button_height(0, self.beginning_position, self.margin, self.height)),
            self.width,
            self.height,
            0,
            'Menu',
            (255, 225, 255),
        )

        self.START_GAME = Button(
            self.screen,
            'menu_button',
            (148, 158, 230),
            (self.center_screen.x - self.width // 2, self.get_button_height(0, self.beginning_position, self.margin, self.height)),
            self.width,
            self.height,
            0,
            'Play',
            (255, 225, 255),
        )

        self.RESUME_GAME = Button(
            self.screen,
            'pause_button',
            (148, 158, 230),
            (self.center_screen.x - self.width // 2, self.get_button_height(0, self.beginning_position, self.margin, self.height)),
            self.width,
            self.height,
            0,
            'Resume',
            (255, 225, 255),
        )

        self.EXIT_GAME = Button(
            self.screen,
            'menu_button',
            (148, 158, 230),
            (self.center_screen.x - self.width // 2, self.get_button_height(1, self.beginning_position, self.margin, self.height)),
            self.width,
            self.height,
            0,
            'Exit',
            (255, 225, 255),
        )

    # Get margin from button position
    def get_button_height(self, but_num:int, start_h:int, margin:int, butt_height:int):
        return start_h + but_num * butt_height + (but_num * 2) * margin

    def create_menu_button(self):
        self.START_GAME.create_button()
        self.EXIT_GAME.create_button()

    def create_links(self):
        self.GIT.create_link()
        self.VK.create_link()
        self.TG.create_link()

    def create_pause_button(self):
        self.RESUME_GAME.create_button()
        self.EXIT_GAME.create_button()

    def create_restart_button(self):
        self.MENU.create_button()

    # Show menu
    def show_menu(self):
        # View menu background
        self.screen.blit(self.background, (0, 0))

        # View Annotation
        self.view_game_name()
        self.create_links()
        self.view_creator()

        # Crate buttons
        self.create_menu_button()

    def show_pause(self):
        # View menu background
        self.screen.blit(self.background, (0, 0))

        # View Annotation
        self.view_pause_text()

        # Crate buttons
        self.create_pause_button()

    def show_restart(self):
        # View menu background
        self.screen.blit(self.background, (0, 0))

        # View Annotation
        self.view_restart_text()

        # Crate buttons
        self.create_restart_button()