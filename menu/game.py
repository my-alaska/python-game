import pygame

from game_classes.level import init_levels
from game_classes.shop import Shop
from game_classes.creature import Hero, init_enemies
from pygame import mixer
import menu


class Game:
    def __init__(self, player_hero: Hero):
        self.player_hero = player_hero
        pygame.init()
        mixer.music.load("../game_contents/python_game_ost.mp3")
        self.volume = 0
        mixer.music.set_volume(self.volume / 10)
        mixer.music.play(-1)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = \
            False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 900, 700
        self.background_image = pygame.image.load("../game_contents/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.font_name = pygame.font.get_default_font()
        self.main_menu = menu.MainMenu(self)
        self.options_menu = menu.OptionsMenu(self)
        self.credits_menu = menu.CreditsMenu(self)
        self.gameplay_menu = menu.GameplayMenu(self)
        self.level_menu = menu.LevelMenu(self)
        self.character_menu = menu.CharacterMenu(self)
        self.stats_menu = menu.StatsMenu(self)
        self.shop_menu = menu.ShopMenu(self)
        self.curr_menu = self.main_menu
        self.shop = Shop()
        self.levels = init_levels(init_enemies(self.init_images()))

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

    def get_level_color(self, level_index):
        if level_index == 1 or self.levels[level_index - 2].completed:
            return 255, 255, 255
        else:
            return 64, 64, 64

    @staticmethod
    def init_images():
        image_w = 200
        image_h = 200
        skeleton = pygame.image.load("../game_contents/skeleton.png")
        skeleton = pygame.transform.scale(skeleton, (image_w, image_h))
        knight = pygame.image.load("../game_contents/knight.png")
        knight = pygame.transform.scale(knight, (image_w, image_h))
        garek = pygame.image.load("../game_contents/hotpot.png")
        garek = pygame.transform.scale(garek, (image_w, image_h))
        slime = pygame.image.load("../game_contents/slime.png")
        slime = pygame.transform.scale(slime, (image_w, image_h))
        return [slime, skeleton, knight, garek]
