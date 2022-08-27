import game_classes.item as itm
from game_classes.creature import Hero, MagicAttackType


class Shop:

    def __init__(self):
        self.items = {
            "miecz 1": itm.Sword(10, 50),
            "miecz 2": itm.Sword(20, 75),
            "miecz 3": itm.Sword(30, 100),
            "zbroja 1": itm.Armor(10, 50),
            "zbroja 2": itm.Armor(20, 75),
            "zbroja 3": itm.Armor(30, 100),
            "mała mikstura": itm.Potion(30, 50),
            "średnia mikstura": itm.Potion(60, 75),
            "duża mikstura": itm.Potion(100, 100),
            "różdżka ognia": itm.Wand(30, MagicAttackType.FIRE, 50),
            "różdżka lodu": itm.Wand(30, MagicAttackType.ICE, 50),
            "różdżka błyskawic": itm.Wand(30, MagicAttackType.SHOCK, 50)
        }

    def sell_item_to_hero(self, item_name, hero: Hero):
        if hero.items[item_name] is not None:
            return 1
        elif hero.gold < self.items[item_name].cost:
            return 2
        else:
            hero.gold -= self.items[item_name].cost
            hero.items[item_name] = self.items[item_name]
            return 0
