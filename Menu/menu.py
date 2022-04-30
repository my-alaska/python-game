import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.curr_menu = self.game.gameplay_menu
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.display.fill(self.game.BLACK)
            self.game.check_events()
            self.check_input()
            self.game.draw_text("Options", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(f"Volume {self.game.volume}", 20, self.volx, self.voly)
            self.blit_screen()

    def change_volume(self):
        if self.game.RIGHT_KEY and self.game.volume != 10:
            self.game.volume += 1
        elif self.game.LEFT_KEY and self.game.volume != 0:
            self.game.volume -= 1

    def check_input(self):
        self.change_volume()
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game

    def check_input(self):
        if self.game.START_KEY or self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def display_menu(self):
        self.run_display = True
        chungus = pygame.image.load("chungus.png")
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display = pygame.transform.scale(chungus, (self.game.DISPLAY_W, self.game.DISPLAY_H))
            self.blit_screen()


class GameplayMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = "Level"
        self.levelx, self.levely = self.mid_w, self.mid_h + 30
        self.characterx, self.charactery = self.mid_w, self.mid_h + 50
        self.statsx, self.statsy = self.mid_w, self.mid_h + 70
        self.shopx, self.shopy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.levelx + self.offset, self.levely)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Game", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Level", 20, self.levelx, self.levely)
            self.game.draw_text("Character", 20, self.characterx, self.charactery)
            self.game.draw_text("Statistics", 20, self.statsx, self.statsy)
            self.game.draw_text("Shop", 20, self.shopx, self.shopy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Level":
                self.cursor_rect.midtop = (self.characterx + self.offset, self.charactery)
                self.state = "Character"
            elif self.state == "Character":
                self.cursor_rect.midtop = (self.statsx + self.offset, self.statsy)
                self.state = "Statistics"
            elif self.state == "Statistics":
                self.cursor_rect.midtop = (self.shopx + self.offset, self.shopy)
                self.state = "Shop"
            elif self.state == "Shop":
                self.cursor_rect.midtop = (self.levelx + self.offset, self.levely)
                self.state = "Level"
        elif self.game.UP_KEY:
            if self.state == "Statistics":
                self.cursor_rect.midtop = (self.characterx + self.offset, self.charactery)
                self.state = "Character"
            elif self.state == "Shop":
                self.cursor_rect.midtop = (self.statsx + self.offset, self.statsy)
                self.state = "Statistics"
            elif self.state == "Level":
                self.cursor_rect.midtop = (self.shopx + self.offset, self.shopy)
                self.state = "Shop"
            elif self.state == "Character":
                self.cursor_rect.midtop = (self.levelx + self.offset, self.levely)
                self.state = "Level"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Level":
                self.game.curr_menu = self.game.level_menu
            elif self.state == "Character":
                self.game.curr_menu = self.game.character_menu
            elif self.state == "Statistics":
                self.game.curr_menu = self.game.stats_menu
            elif self.state == "Shop":
                self.game.curr_menu = self.game.shop_menu
            self.run_display = False
        elif self.game.BACK_KEY:
            self.run_display = False
            self.game.curr_menu = self.game.main_menu


class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = 1
        self.x1, self.y1 = self.mid_w, self.mid_h + 30
        self.x2, self.y2 = self.mid_w, self.mid_h + 50
        self.x3, self.y3 = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.x1 + self.offset, self.y1)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.state == 1:
                i = 2
            elif self.state == 10:
                i = 9
            else:
                i = self.state
            self.game.draw_text("Select Level", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(f"level {i - 1}", 20, self.x1, self.y1)
            self.game.draw_text(f"level {i}", 20, self.x2, self.y2)
            self.game.draw_text(f"level {i + 1}", 20, self.x3, self.y3)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.state == 1:
            self.cursor_rect.midtop = (self.x1 + self.offset, self.y1)
        elif self.state == 10:
            self.cursor_rect.midtop = (self.x3 + self.offset, self.y3)
        elif self.state == 9 or self.state == 2:
            self.cursor_rect.midtop = (self.x2 + self.offset, self.y2)

    def update_state(self):
        if self.game.DOWN_KEY and self.state != 10:
            self.state += 1
            self.move_cursor()
        elif self.game.UP_KEY and self.state != 1:
            self.state -= 1
            self.move_cursor()

    def check_input(self):
        self.update_state()
        if self.game.START_KEY:
            pass  # TODO włączanie poziomów
        elif self.game.BACK_KEY:
            self.run_display = False
            self.game.curr_menu = self.game.gameplay_menu


class CharacterMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = "Broń"
        self.cursor_state = 1
        self.x1, self.y1 = self.mid_w, self.mid_h + 30
        self.x2, self.y2 = self.mid_w, self.mid_h + 50
        self.x3, self.y3 = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.x1 + self.offset, self.y1)
        self.o = ["miecz 1", "miecz 2", "miecz 3"]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(self.state, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(self.o[0], 20, self.x1, self.y1)
            self.game.draw_text(self.o[1], 20, self.x2, self.y2)
            self.game.draw_text(self.o[2], 20, self.x3, self.y3)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.cursor_state == 1:
            self.cursor_rect.midtop = (self.x1 + self.offset, self.y1)
        elif self.cursor_state == 2:
            self.cursor_rect.midtop = (self.x2 + self.offset, self.y2)
        elif self.cursor_state == 3:
            self.cursor_rect.midtop = (self.x3 + self.offset, self.y3)

    def update_state(self):
        if self.game.RIGHT_KEY:
            if self.state == "Broń":
                self.state = "Różdżka"
                self.o = ["różdżka ognia", "różdżka lodu", "różdżka błyskawic"]
            elif self.state == "Różdżka":
                self.state = "Zbroja"
                self.o = ["zbroja 1", "zbroja 2", "zbroja 3"]
            elif self.state == "Zbroja":
                self.state = "Broń"
                self.o = ["miecz 1", "miecz 2", "miecz 3"]
        elif self.game.LEFT_KEY:
            if self.state == "Zbroja":
                self.state = "Różdżka"
                self.o = ["różdżka ognia", "różdżka lodu", "różdżka błyskawic"]
            elif self.state == "Broń":
                self.state = "Zbroja"
                self.o = ["zbroja 1", "zbroja 2", "zbroja 3"]
            elif self.state == "Różdżka":
                self.state = "Broń"
                self.o = ["miecz 1", "miecz 2", "miecz 3"]
        elif self.game.UP_KEY and self.cursor_state != 1:
            self.cursor_state -= 1
            self.move_cursor()
        elif self.game.DOWN_KEY and self.cursor_state != 3:
            self.cursor_state += 1
            self.move_cursor()

    def check_input(self):
        self.update_state()
        if self.game.START_KEY:
            print("nie posiadasz", self.o[self.cursor_state - 1])  # TODO włączanie poziomów
        elif self.game.BACK_KEY:
            self.run_display = False
            self.game.curr_menu = self.game.gameplay_menu


class StatsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.hpx, self.hpy = self.mid_w, self.mid_h + 30
        self.mpx, self.mpy = self.mid_w, self.mid_h + 50
        self.strx, self.stry = self.mid_w, self.mid_h + 70
        self.conx, self.cony = self.mid_w, self.mid_h + 90
        self.speedx, self.speedy = self.mid_w, self.mid_h + 110
        self.mrx, self.mry = self.mid_w, self.mid_h + 130

    def check_input(self):
        if self.game.START_KEY or self.game.BACK_KEY:
            self.game.curr_menu = self.game.gameplay_menu
            self.run_display = False

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Statistics", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(f"hit points {0}", 20, self.hpx, self.hpy)
            self.game.draw_text(f"magic points {0}", 20, self.mpx, self.mpy)
            self.game.draw_text(f"strength {0}", 20, self.strx, self.stry)
            self.game.draw_text(f"constitution {0}", 20, self.conx, self.cony)
            self.game.draw_text(f"speed {0}", 20, self.speedx, self.speedy)
            self.game.draw_text(f"fire/ice/lightning resistance {0}/{0}/{0}", 20, self.mrx, self.mry)
            self.blit_screen()


class ShopMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = "Broń"
        self.cursor_state = 1
        self.x1, self.y1 = self.mid_w, self.mid_h + 30
        self.x2, self.y2 = self.mid_w, self.mid_h + 50
        self.x3, self.y3 = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.x1 + self.offset, self.y1)
        self.o = ["miecz 1", "miecz 2", "miecz 3"]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(self.state, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text(self.o[0], 20, self.x1, self.y1)
            self.game.draw_text(self.o[1], 20, self.x2, self.y2)
            self.game.draw_text(self.o[2], 20, self.x3, self.y3)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.cursor_state == 1:
            self.cursor_rect.midtop = (self.x1 + self.offset, self.y1)
        elif self.cursor_state == 2:
            self.cursor_rect.midtop = (self.x2 + self.offset, self.y2)
        elif self.cursor_state == 3:
            self.cursor_rect.midtop = (self.x3 + self.offset, self.y3)

    def update_state(self):
        if self.game.RIGHT_KEY:
            if self.state == "Broń":
                self.state = "Różdżka"
                self.o = ["różdżka ognia", "różdżka lodu", "różdżka błyskawic"]
            elif self.state == "Różdżka":
                self.state = "Zbroja"
                self.o = ["zbroja 1", "zbroja 2", "zbroja 3"]
            elif self.state == "Zbroja":
                self.state = "Mikstura"
                self.o = ["mała mikstura", "średnia mikstura", "duża mikstura"]
            elif self.state == "Mikstura":
                self.state = "Broń"
                self.o = ["miecz 1", "miecz 2", "miecz 3"]
        elif self.game.LEFT_KEY:
            if self.state == "Zbroja":
                self.state = "Różdżka"
                self.o = ["różdżka ognia", "różdżka lodu", "różdżka błyskawic"]
            elif self.state == "Mikstura":
                self.state = "Zbroja"
                self.o = ["zbroja 1", "zbroja 2", "zbroja 3"]
            elif self.state == "Różdżka":
                self.state = "Broń"
                self.o = ["miecz 1", "miecz 2", "miecz 3"]
            elif self.state == "Broń":
                self.o = ["mała mikstura", "średnia mikstura", "duża mikstura"]
        elif self.game.UP_KEY and self.cursor_state != 1:
            self.cursor_state -= 1
            self.move_cursor()
        elif self.game.DOWN_KEY and self.cursor_state != 3:
            self.cursor_state += 1
            self.move_cursor()

    def check_input(self):
        self.update_state()
        if self.game.START_KEY:
            print("za mało złota by kupić przedmiot:", self.o[self.cursor_state - 1])
            # TODO kupowanie przemdiotów
        elif self.game.BACK_KEY:
            self.run_display = False
            self.game.curr_menu = self.game.gameplay_menu
