import pygame
from Game_classes.creature import Enemy

class Fight:
    def __init__(self, hero, state, game):
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.hero = hero
        self.enemy = Enemy() #TODO losowanie przeskalowanego wroga
        self.state = state #TODO poziom stwora
        self.action_type = None #do zapisywania jaki ruch chce player
        self.hero_state = 0
        self.enemy_state = 0
        self.timer_running = True   # kiedy jest true, paski hero_state i enemy_state się łądują
        #inna opcja - stworzyć mini okienko w loopie - główna pętla gry ma używać sleepów. raz na pętlę dodajemy
        #agility *0.01 do hero state i enemy state

        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.fight_is_on = True
        self.players_turn = True

        self.enemy_image = pygame.image.load("chungus.png") #todo załadowanie image wroga
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.game.DISPLAY_W / 4, self.game.DISPLAY_H / 4))
        self.attack_opt_x_coord = self.game.DISPLAY_W / 8
        self.defend_opt_x_coord = self.game.DISPLAY_W / 8 * 3
        self.magic_option_x_coord = self.game.DISPLAY_W / 8 * 5
        self.potion_opt_x_coord = self.game.DISPLAY_W / 8 * 7
        self.opt_y_coord = self.game.DISPLAY_H / 4 * 3


    def fight_loop(self):
        while self.fight_is_on:
            self.game.reset_keys()
            self.display_game_scene()
            pygame.time.wait(1000)
            self.hero_action()
            # if self.enemy.is_dead():
            #     self.fight_is_on = False
            #     break
            # pygame.time.wait(1000)
            # self.display_game_scene()
            # self.enemy_action()
            # pygame.time.wait(1000)
            self.movement_regeneration()
            print('dupa')

    def display_game_scene(self):
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text("hero: health points: " + str(self.hero.health_points) + "/100 " +
                            "move points: " + str(self.hero_state) + "/100",
                            20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.game.draw_text("enemy: health points: " + str(self.hero.health_points) + "/100 " +
                            "move points: " + str(self.hero_state) + "/100",
                            20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
        # self.game.draw_text("Start Game", 20, self.startx, self.starty)
        # self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
        # self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
        self.game.window.blit(self.game.display, (0, 0))
        self.game.window.blit(self.enemy_image, (3 * self.game.DISPLAY_W / 8, 50))
        pygame.display.update()

    def display_fight_scene(self):
        self.game.check_events()
        self.check_input()
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text("hero: health points: " + str(self.hero.health_points) + "/100 " +
                            "move points: " + str(self.hero_state) + "/100",
                            20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.game.draw_text("enemy: health points: " + str(self.hero.health_points) + "/100 " +
                            "move points: " + str(self.hero_state) + "/100",
                            20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
        self.game.draw_text("Attack", 20, self.attack_opt_x_coord, self.opt_y_coord)
        self.game.draw_text("Defend", 20, self.defend_opt_x_coord, self.opt_y_coord)
        self.game.draw_text("Magic", 20, self.magic_option_x_coord, self.opt_y_coord)
        self.game.draw_text("Potion", 20, self.potion_opt_x_coord, self.opt_y_coord)
        self.game.window.blit(self.game.display, (0, 0))
        self.game.window.blit(self.enemy_image, (3 * self.game.DISPLAY_W / 8, 50))
        pygame.display.update()

    def check_input(self):
        pass

    def move_cursor(self):
        if self.game.RIGHT_KEY:
            if self.state == "Attack":
                self.cursor_rect.midtop = (self.defend_opt_x_coord - 20, self.opt_y_coord)
                self.state = "Defend"
            elif self.state == "Defend":
                self.cursor_rect.midtop = (self.magic_option_x_coord - 20, self.opt_y_coord)
                self.state = "Magic"
            elif self.state == "Magic":
                self.cursor_rect.midtop = (self.potion_opt_x_coord - 20, self.opt_y_coord)
                self.state = "Potion"
            elif self.state == "Potion":
                self.cursor_rect.midtop = (self.attack_opt_x_coord - 20, self.opt_y_coord)
                self.state = "Attack"
        elif self.game.UP_KEY:
            if self.state == "Attack":
                self.cursor_rect.midtop = (self.potion_opt_x_coord - 20, self.opt_y_coord)
                self.state = "Potion"
            elif self.state == "Defend":
                self.cursor_rect.midtop = (self.attack_opt_x_coord - 20, self.opt_y_coord)
                self.state = "Attack"
            elif self.state == "Magic":
                self.cursor_rect.midtop = (self.defend_opt_x_coord - 20, self.opt_y_coord)
                self.state = "Defend"
            elif self.state == "Potion":
                self.cursor_rect.midtop = (self.magic_option_x_coord - 20, self.opt_y_coord)
                self.state = "Magic"

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def display_turn_info(self, info):
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text(info, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def hero_action(self):#TODO ograniczenia na atakowanie np magiczne albo na poty
        if self.hero_state >= 100:
            player_still_choosing = True
            while True:
                self.display_fight_scene()

            # chosen_action = self.players_turn_menu.display_game()
            # if chosen_action == "Melee attack":
            #     self.hero.attack(self.enemy)
            # elif chosen_action == "Magic attack":
            #     self.hero.magic_attack(self.enemy)
            # elif chosen_action == "Use potion":
            #     self.hero.use_potion()
            # self.display_turn_info('hero makes move')

    def movement_regeneration(self):
        self.hero_state = min(self.hero_state + self.hero.agility, 100)
        self.enemy_state = min(self.enemy_state + self.enemy.agility, 100)

    def enemy_action(self):
        action = self.enemy.strategy.make_move()
        print(action)
        if action == "melee attack" and self.enemy.stamina_points >= 100:
            self.enemy.attack(self.hero)
            self.display_turn_info('enemy makes move')
        elif action == "magic attack" and self.enemy.mana_points >= 100:
            self.enemy.magic_attack(self.hero)
            self.display_turn_info('enemy makes move')
