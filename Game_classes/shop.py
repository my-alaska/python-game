from Game_classes.creature import Hero
from Game_classes.item import Item, ItemType


class Shop:

    def __init__(self):
        items = []

    def sell_item_to_hero(self, item: Item, hero: Hero):
        hero.gold -= item.cost
        if item.item_type == ItemType.ARMOR:
            hero.active_armor = item
        elif item.item_type == ItemType.SWORD:
            hero.active_sword = item
        elif item.item_type == ItemType.WAND:
            hero.active_wand = item
        else:
            hero.active_potion = item
