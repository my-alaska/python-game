from game import Game
from Game_classes.creature import Hero

p = Hero()
g = Game(p)

while g.running:
    g.curr_menu.display_game()
    g.game_loop()