from enum import Enum

from Game_classes.creature import Hero

class Item():

    def __init__(self, cost, item_type):
        self.cost = cost
        self.item_type = item_type

class Armor(Item):

    def __init__(self, armor_bonus, cost):
        Item.__init__(self, cost, Item_type.ARMOR)
        self.armor_bonus = armor_bonus

class Sword(Item):

    def __init__(self, strength_bonus, attack_stamina_cost, cost):
        Item.__init__(self, cost, Item_type.SWORD)
        self.strength_bonus = strength_bonus
        self.attack_stamina_cost = attack_stamina_cost


class Wand(Item):
    def __init__(self, power_bonus, magic_type, cost):
        Item.__init__(self, cost, Item_type.WAND)
        self.power_bonus = power_bonus
        self.magic_type = magic_type


class Potion(Item):

    def __init__(self, health_restored, cost):
        Item.__init__(self, cost, Item_type.WAND)
        self.health_restored = health_restored

    def heal_hero(self, hero: Hero):
        hero.health_points += self.health_restored

class Item_type(Enum):
    SWORD = 1
    ARMOR = 2
    WAND = 3
    POTION = 4

