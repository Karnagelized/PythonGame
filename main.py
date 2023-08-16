
import pygame
import sys
import random
import time
from settings import GAME_NAME, SIZE, FPS, FONT_LINK, GAME_SETTINGS, WIDTH
from level import Level
from menu import Menu
from story import Prolog, Ending


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load('data/icon.png'))

        # General
        self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        self.screen_center = pygame.math.Vector2(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2)
        self.clock = pygame.time.Clock()
        self.fps = self.clock.get_fps()
        self.fps_update = 10
        self.screen_type = 'menu'

        # Init Menu
        self.menu = Menu(self.screen, self.screen_center)

        # Init Restart
        self.restart = Menu(self.screen, self.screen_center, False)

        # Story
        self.prolog = Prolog()
        self.ending = Ending()

        # Init Level
        self.level = Level()

    def IS_MENU(self):
        return self.screen_type == 'menu'

    def IS_PROLOG(self):
        return self.screen_type == 'prolog'

    def IS_GAME(self):
        return self.screen_type == 'game'

    def IS_PAUSED(self):
        return self.screen_type == 'pause'

    def IS_RESTARTED(self):
        return self.screen_type == 'restart'

    def IS_ENDING(self):
        return self.screen_type == 'ending'

    def game_info(self):
        # View FPS on screen
        if pygame.time.get_ticks() // 100 % self.fps_update == 0:
            self.fps = self.clock.get_fps()

        # Change FPS color from his amount
        if self.fps > 45:
            _fps_color = (0, 255, 0)
        elif 30 < self.fps <= 45:
            _fps_color = (255, 128, 0)
        else:
            _fps_color = (255, 0, 0)

        _font = pygame.font.Font(FONT_LINK, 24)
        _fps = _font.render(f'FPS: {int(self.clock.get_fps())}', 0, _fps_color)
        self.screen.blit(_fps, (WIDTH - _fps.get_width() - 10, 10))


    def restart_game(self):
        self.screen_type = 'menu'
        self.menu = Menu(self.screen, self.screen_center)
        self.prolog = Prolog()
        self.level = Level()


    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT or keys[pygame.K_HOME]:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Menu
                    if self.IS_MENU():
                        # Buttons
                        if self.menu.START_GAME.pressed(pygame.mouse.get_pos()):
                            self.menu.switch_sound()
                            self.screen_type = 'prolog'
                        elif self.menu.EXIT_GAME.pressed(pygame.mouse.get_pos()):
                            self.exit_game()

                        # Links
                        self.menu.GIT.pressed(pygame.mouse.get_pos())
                        self.menu.VK.pressed(pygame.mouse.get_pos())
                        self.menu.TG.pressed(pygame.mouse.get_pos())

                    # Pause
                    if self.IS_PAUSED():
                        # Buttons
                        if self.menu.RESUME_GAME.pressed(pygame.mouse.get_pos()):
                            self.screen_type = 'game'
                        elif self.menu.EXIT_GAME.pressed(pygame.mouse.get_pos()):
                            self.exit_game()

                    # Restart game
                    if self.IS_RESTARTED():
                        if self.menu.MENU.pressed(pygame.mouse.get_pos()):
                            self.restart_game()

                elif self.IS_GAME() and keys[pygame.K_ESCAPE]:
                    self.screen_type = 'pause'
                elif self.IS_GAME() and keys[pygame.K_F3]:
                    GAME_SETTINGS.GAME_INFO = not GAME_SETTINGS.GAME_INFO
                elif self.IS_ENDING() and keys[pygame.K_r]:
                    self.restart_game()


            # Activate screen from screen_type
            if self.IS_MENU():
                self.menu.show_menu()

                # Hover
                self.menu.START_GAME.hovering(pygame.mouse.get_pos())
                self.menu.EXIT_GAME.hovering(pygame.mouse.get_pos())
                self.menu.GIT.hovering(pygame.mouse.get_pos())
                self.menu.VK.hovering(pygame.mouse.get_pos())
                self.menu.TG.hovering(pygame.mouse.get_pos())
            elif self.IS_PROLOG():
                if not self.prolog.annotation.finished:
                    self.prolog.run()

                # End prolog
                if self.prolog.annotation.finished or keys[pygame.K_RETURN]:
                    self.screen_type = 'game'
            elif self.IS_PAUSED():
                self.menu.show_pause()
                self.menu.RESUME_GAME.hovering(pygame.mouse.get_pos())
                self.menu.EXIT_GAME.hovering(pygame.mouse.get_pos())
            elif self.IS_GAME():
                self.level.run()

                # View game info
                if GAME_SETTINGS.GAME_INFO:
                    self.game_info()

                # Restart game
                if self.level.player.is_die:
                    self.screen_type = 'restart'

                # End game
                if self.level.game_compl:
                    if self.level._alpha == 255:
                        self.level.background_suond.stop()
                        self.screen_type = 'ending'
            elif self.IS_RESTARTED():
                self.menu.show_restart()
                self.menu.MENU.hovering(pygame.mouse.get_pos())
            elif self.IS_ENDING():
                self.ending.run(self.level.player.statistic, self.level.duration)

            pygame.display.update()
            self.clock.tick(60)
            pygame.display.set_caption(f'{GAME_NAME}')


if __name__ == '__main__':
    Game().run()