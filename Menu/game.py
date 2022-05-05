import pygame
from menu import MainMenu, OptionsMenu, CreditsMenu, GameplayMenu, LevelMenu, CharacterMenu, StatsMenu, ShopMenu
from Game_classes.shop import Shop
from Game_classes.creature import Hero


class Game():
    def __init__(self, player_hero: Hero):
        self.player_hero = player_hero
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = \
            False, False, False, False, False, False
        self.volume = 10
        self.DISPLAY_W, self.DISPLAY_H = 900, 700
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.font_name = pygame.font.get_default_font()
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.gameplay_menu = GameplayMenu(self)
        self.level_menu = LevelMenu(self)
        self.character_menu = CharacterMenu(self)
        self.stats_menu = StatsMenu(self)
        self.shop_menu = ShopMenu(self)
        self.curr_menu = self.main_menu
        self.shop = Shop()

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text('COMING SOON', 50, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = \
            False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

