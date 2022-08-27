import pygame


class Fight:
    def __init__(self, hero, game, level):
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.hero = hero
        self.level = level
        self.enemy = level.enemy
        self.gold = level.gold_given
        self.state = "Attack"
        self.action_type = None
        self.hero_state = 0
        self.enemy_state = 0
        self.timer_running = True
        self.potion_used = False
        self.defending = False

        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.fight_is_on = True
        self.players_turn = True
        self.attack_opt_x_coord = self.game.DISPLAY_W / 8
        self.defend_opt_x_coord = self.game.DISPLAY_W / 8 * 3
        self.magic_option_x_coord = self.game.DISPLAY_W / 8 * 5
        self.potion_opt_x_coord = self.game.DISPLAY_W / 8 * 7
        self.opt_y_coord = self.game.DISPLAY_H / 4 * 3

    def fight_loop(self):
        while self.fight_is_on:
            self.game.reset_keys()
            self.display_game_scene()
            pygame.time.wait(500)

            if self.hero_state >= 100:
                curr_state, possible_attack = self.hero_action()
            else:
                curr_state = None
            if curr_state == "Attack" or curr_state == "Magic":
                self.handle_attack(self.enemy, curr_state, possible_attack)

            if self.enemy.is_dead():
                self.end_fight_good(self.gold)
                break

            self.display_game_scene()
            curr_state, possible_attack = self.enemy_action()
            if curr_state == "Attack" or curr_state == "Magic":
                self.handle_attack(self.hero, curr_state, possible_attack)

            if self.hero.is_dead():
                self.end_fight_bad()
                break
            self.movement_regeneration()

    def display_game_scene(self):
        self.game.display.blit(self.game.background_image, (0, 0))
        pygame.draw.rect(self.game.display, (255, 0, 0),
                         ((self.game.DISPLAY_W / 2 - 100), 350, 200 * (self.enemy.health_points / 100), 15), 10)
        pygame.draw.rect(self.game.display, (255, 255, 0),
                         ((self.game.DISPLAY_W / 2 - 100), 370, 200 * (self.enemy_state / 100), 15), 10)
        pygame.draw.rect(self.game.display, (255, 0, 0),
                         (30, self.opt_y_coord + 50, 200 * (self.hero.health_points / 100), 15), 10)
        pygame.draw.rect(self.game.display, (255, 255, 0),
                         (30, self.opt_y_coord + 70, 200 * (self.hero_state / 100), 15), 10)
        self.game.draw_text("Attack", 20, self.attack_opt_x_coord, self.opt_y_coord, (64, 64, 64))
        self.game.draw_text("Defend", 20, self.defend_opt_x_coord, self.opt_y_coord, (64, 64, 64))
        self.game.draw_text("Magic", 20, self.magic_option_x_coord, self.opt_y_coord, (64, 64, 64))
        self.game.draw_text("Potion", 20, self.potion_opt_x_coord, self.opt_y_coord, (64, 64, 64))
        self.game.window.blit(self.game.display, (0, 0))
        self.game.window.blit(self.enemy.image, (self.game.DISPLAY_W / 2 - 100, 150))
        pygame.display.update()

    def display_fight_scene(self):
        self.game.display.blit(self.game.background_image, (0, 0))  # ustawiam tło
        pygame.draw.rect(self.game.display, (255, 0, 0),
                         ((self.game.DISPLAY_W / 2 - 100), 350, 200 * (self.enemy.health_points / 100), 15), 10)
        pygame.draw.rect(self.game.display, (255, 255, 0),
                         ((self.game.DISPLAY_W / 2 - 100), 370, 200 * (self.enemy_state / 100), 15), 10)
        pygame.draw.rect(self.game.display, (255, 0, 0),
                         (30, self.opt_y_coord + 50, 200 * (self.hero.health_points / 100), 15), 10)
        pygame.draw.rect(self.game.display, (255, 255, 0),
                         (30, self.opt_y_coord + 70, 200 * (self.hero_state / 100), 15), 10)
        self.game.draw_text("Attack", 20, self.attack_opt_x_coord, self.opt_y_coord, self.get_color("Attack"))
        self.game.draw_text("Defend", 20, self.defend_opt_x_coord, self.opt_y_coord, self.get_color("Defend"))
        self.game.draw_text("Magic", 20, self.magic_option_x_coord, self.opt_y_coord, self.get_color("Magic"))
        self.game.draw_text("Potion", 20, self.potion_opt_x_coord, self.opt_y_coord, self.get_color("Potion"))
        self.game.window.blit(self.game.display, (0, 0))
        self.game.window.blit(self.enemy.image, (self.game.DISPLAY_W / 2 - 100, 150))
        pygame.display.update()

    def check_input(self):
        self.move_cursor()
        if self.hero_state >= 100 and self.game.START_KEY:
            if self.state == "Attack" or self.state == "Defend":
                return True
            elif self.state == "Magic":
                if self.hero.mana_points < 100:
                    print("not enough mana")
                if self.hero.active_wand is None:
                    print("you dont have a wand")
                return self.hero.mana_points >= 100 and self.hero.active_wand is not None
            else:
                if self.potion_used:
                    print("You already used your potion!")
                if self.hero.active_potion is None:
                    print("you dont have any potion")
                return not self.potion_used and self.hero.active_potion is not None
        else:
            return False

    def move_cursor(self):
        if self.game.RIGHT_KEY:
            if self.state == "Attack":
                self.state = "Defend"
            elif self.state == "Defend":
                self.state = "Magic"
            elif self.state == "Magic":
                self.state = "Potion"
            elif self.state == "Potion":
                self.state = "Attack"
        elif self.game.LEFT_KEY:
            if self.state == "Attack":
                self.state = "Potion"
            elif self.state == "Defend":
                self.state = "Attack"
            elif self.state == "Magic":
                self.state = "Defend"
            elif self.state == "Potion":
                self.state = "Magic"

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def get_color(self, string):
        if self.state == string:
            return 255, 0, 0
        elif string == "Magic" and self.hero.active_wand is None:
            return 64, 64, 64
        elif string == "Potion" and self.hero.active_potion is None:
            return 64, 64, 64

        else:
            return 255, 255, 255

    def display_turn_info(self, info):
        self.game.display.blit(self.game.background_image, (0, 0))  # ustawiam tło
        self.game.draw_text(info, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def hero_action(
            self):  # TODO zrob ze resetowanie obrony na turze ograniczenia na atakowanie np magiczne albo na poty
        self.state = "Attack"
        self.game.check_events()
        self.game.reset_keys()
        if self.hero_state >= 100:
            self.defending = False
            while True:

                self.game.reset_keys()
                self.game.check_events()
                if self.check_input():
                    break
                self.display_fight_scene()
            self.hero_state = 0
            if self.state == "Attack" or self.state == "Magic":
                return self.state, self.hero.attack(self.state)
            elif self.state == "Potion":
                self.hero.use_potion()
                self.potion_used = True
            else:
                self.defending = True
            return self.state, None
        return None, None

    def handle_attack(self, targeted_creature, attack_type, attack_stats):
        attack_damage, magic_type = attack_stats
        if self.defending:
            attack_damage //= 2
        attack_damage = targeted_creature.reduce_damage(attack_type, attack_damage, magic_type)
        targeted_creature.receive_injuries(attack_damage)

    def movement_regeneration(self):
        self.hero.mana_points = min(100, self.hero.mana_points + 10)
        self.hero_state = min(self.hero_state + self.hero.agility, 100)
        self.enemy_state = min(self.enemy_state + self.enemy.agility, 100)

    def enemy_action(self):
        if self.enemy_state >= 100:
            action = self.enemy.strategy.make_move()
            self.enemy_state = 0
            return action, self.enemy.attack(action)
        return None, None

    def end_fight_good(self, gold):
        self.fight_is_on = False
        self.hero.gold += gold
        self.level.completed = True
        self.hero.reset_creature_stats()
        self.enemy.reset_creature_stats()

    def end_fight_bad(self):
        self.fight_is_on = False
        self.hero.reset_creature_stats()
        self.enemy.reset_creature_stats()
