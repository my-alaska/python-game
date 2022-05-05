from Game_classes.creature import Hero
from Game_classes.item import Item, ItemType
import Game_classes.item as itm


class Shop:

    def __init__(self):
        self.items = {
            "miecz 1": itm.Sword(10,50),
            "miecz 2": itm.Sword(20,75),
            "miecz 3": itm.Sword(30,100),
            "zbroja 1": itm.Armor(10,50),
            "zbroja 2": itm.Armor(20,75),
            "zbroja 3": itm.Armor(30,100),
            "mała mikstura": itm.Potion(30,50),
            "średnia mikstura": itm.Potion(60,75),
            "duża mikstura": itm.Potion(100,100),
            "różdżka ognia": itm.Wand(30,"fire",50),
            "różdżka lodu": itm.Wand(30,"ice",50),
            "różdżka błyskawic": itm.Wand(30,"lightning",50)
        }

    def sell_item_to_hero(self, item_name, hero: Hero):
        if hero.items[item_name] is not None:
            print("masz już ten przedmiot")
            return 1
        elif hero.gold < self.items[item_name].cost:
            print("za mało złota")
            return 2
        else:
            hero.gold -= self.items[item_name].cost
            hero.items[item_name] = self.items[item_name]
            return 0



        # hero.gold -= item.cost
        # if item.item_type == ItemType.ARMOR:
        #     hero.active_armor = item
        # elif item.item_type == ItemType.SWORD:
        #     hero.active_sword = item
        # elif item.item_type == ItemType.WAND:
        #     hero.active_wand = item
        # else:
        #     hero.active_potion = item
        #