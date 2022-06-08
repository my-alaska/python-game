from game import Game
from Game_classes.creature import Hero


def main():
    p = Hero()
    g = Game(p)

    while g.running:
        g.curr_menu.display_game()
        g.game_loop()


if __name__ == "__main__":
    main()
