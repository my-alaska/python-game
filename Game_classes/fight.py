import pygame
from Game_classes.creature import Enemy

class Fight:
    def __init__(self, hero, state, game):
        self.hero = hero

        self.enemy = Enemy()

        self.hero_state = 0
        self.enemy_state = 0
        self.timer_running = True   # kiedy jest true, paski hero_state i enemy_state się łądują
        #inna opcja - stworzyć mini okienko w loopie - główna pętla gry ma używać sleepów. raz na pętlę dodajemy
        #agility *0.01 do hero state i enemy state

        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.fight_is_on = True
        self.players_turn = True



    def fight_loop(self):
        while self.fight_is_on:
            self.game.reset_keys()
            self.display_game_scene()
            pygame.time.wait(1000)
            self.hero_action()
            if self.enemy.is_dead():
                self.fight_is_on = False
                break
            pygame.time.wait(1000)
            self.display_game_scene()
            self.enemy_action()
            pygame.time.wait(1000)
            self.action_regeneration()

    def display_game_scene(self):
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text('hero - health: ' + str(self.hero.health_points) + ' stamina: ' + str(self.hero.stamina_points) + ' mana: ' + str(self.hero.mana_points)
                            , 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
        self.game.draw_text(
            'enemy - health: ' + str(self.enemy.health_points) + ' stamina: ' + str(self.enemy.stamina_points) + ' mana: ' + str(self.enemy.mana_points)
            , 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4 * 3)
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def display_turn_info(self, info):
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text(info, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()

    def hero_action(self):#TODO ograniczenia na atakowanie np magiczne albo na poty
        if self.hero.stamina_points >= 100:
            chosen_action = self.players_turn_menu.display_game()
            if chosen_action == "Melee attack":
                self.hero.attack(self.enemy)
            elif chosen_action == "Magic attack":
                self.hero.magic_attack(self.enemy)
            elif chosen_action == "Use potion":
                self.hero.use_potion()
            self.display_turn_info('hero makes move')

    def action_regeneration(self):
        self.hero.regenerate_stamina()
        self.hero.regenerate_mana()
        self.enemy.regenerate_stamina()
        self.enemy.regenerate_mana()

    def enemy_action(self):
        action = self.enemy.strategy.make_move()
        print(action)
        if action == "melee attack" and self.enemy.stamina_points >= 100:
            self.enemy.attack(self.hero)
            self.display_turn_info('enemy makes move')
        elif action == "magic attack" and self.enemy.mana_points >= 100:
            self.enemy.magic_attack(self.hero)
            self.display_turn_info('enemy makes move')
