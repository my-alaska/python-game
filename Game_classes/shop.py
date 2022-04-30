from Game_classes.creature import Hero
from Game_classes.item import Item, Item_type


class Shop():

    def __init__(self):
        items = []

    def sell_item_to_hero(self, item: Item, hero: Hero):
        hero.gold -= item.cost
        if item.item_type == Item_type.ARMOR:
            hero.active_armor = item
        elif item.item_type == Item_type.SWORD:
            hero.active_sword = item
        elif item.item_type == Item_type.WAND:
            hero.active_wand = item
        else:
            hero.active_potion = item
