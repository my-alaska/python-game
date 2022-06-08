def init_levels(enemies):
    levels = [Level(enemies[i - 1], i * 100) for i in range(1, 11)]
    return levels


class Level:
    def __init__(self, enemy, gold):
        self.enemy = enemy
        self.completed = False
        self.gold_given = gold
