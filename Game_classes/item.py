from enum import Enum


def init_inventory():
    inventory = {
        "miecz 1": None,
        "miecz 2": None,
        "miecz 3": None,
        "zbroja 1": None,
        "zbroja 2": None,
        "zbroja 3": None,
        "mała mikstura": None,
        "średnia mikstura": None,
        "duża mikstura": None,
        "różdżka ognia": None,
        "różdżka lodu": None,
        "różdżka błyskawic": None
    }
    return inventory


class Item:
    def __init__(self, cost, item_type):
        self.cost = cost
        self.item_type = item_type


class Armor(Item):
    def __init__(self, armor_bonus, cost):
        Item.__init__(self, cost, ItemType.ARMOR)
        self.armor_bonus = armor_bonus


class Sword(Item):

    def __init__(self, strength_bonus, cost):
        Item.__init__(self, cost, ItemType.SWORD)
        self.strength_bonus = strength_bonus


class Wand(Item):
    def __init__(self, power_bonus, magic_type, cost):
        Item.__init__(self, cost, ItemType.WAND)
        self.power_bonus = power_bonus
        self.magic_type = magic_type


class Potion(Item):

    def __init__(self, health_restored, cost):
        Item.__init__(self, cost, ItemType.POTION)
        self.health_restored = health_restored

    def heal_hero(self, hero):
        hero.health_points = max(self.health_restored + hero.health_points, 100)


class ItemType(Enum):
    SWORD = 1
    ARMOR = 2
    WAND = 3
    POTION = 4
