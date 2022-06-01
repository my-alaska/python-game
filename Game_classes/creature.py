from typing import List

from Game_classes.item import Sword, Armor, Wand, Potion
from enum import Enum
from Game_classes.item import init_inventory, ItemType

def init_enemies(images):
    moves = [["Attack", "Attack", "Magic"], ["Attack", "Magic"], ["Attack", "Attack", "Defend"], ["Magic"]]
    enemies = [
        Enemy(images[0], 100, 10, 10, 5, 10, MagicResistance(0.5, 0, 0), MagicAttackType.FIRE, Strategy(moves[0])),
        Enemy(images[1], 100, 20, 20, 5, 15, MagicResistance(0.5, 0.5, 0), MagicAttackType.FIRE, Strategy(moves[1])),
        Enemy(images[2], 100, 40, 0, 20, 5, MagicResistance(0, 0, 0), MagicAttackType.FIRE, Strategy(moves[2])),
        Enemy(images[0], 100, 30, 30, 15, 10, MagicResistance(0, 0.5, 0), MagicAttackType.FIRE, Strategy(moves[0])),
        Enemy(images[1], 100, 40, 40, 5, 15, MagicResistance(0.5, 0.5, 0), MagicAttackType.FIRE, Strategy(moves[1])),
        Enemy(images[2], 100, 60, 0, 30, 5, MagicResistance(0, 0, 0), MagicAttackType.FIRE, Strategy(moves[2])),
        Enemy(images[0], 100, 40, 40, 20, 10, MagicResistance(0, 0, 0.5), MagicAttackType.FIRE, Strategy(moves[0])),
        Enemy(images[1], 100, 60, 60, 5, 15, MagicResistance(0, 0.5, 0.5), MagicAttackType.FIRE, Strategy(moves[1])),
        Enemy(images[2], 100, 90, 0, 45, 5, MagicResistance(0, 0, 0), MagicAttackType.FIRE, Strategy(moves[2])),
        Enemy(images[3], 100, 100, 100, 40, 10, MagicResistance(0.5, 0.5, 0.5), MagicAttackType.FIRE, Strategy(moves[3]))
    ]
    return enemies


class MagicAttackType(Enum):
    FIRE = 1
    ICE = 2
    SHOCK = 3


class MagicResistance:

    def __init__(self, fire_resistance=0.0, ice_resistance=0.0, shock_resistance=0.0):
        self.fire_resistance = fire_resistance
        self.ice_resistance = ice_resistance
        self.shock_resistance = shock_resistance

    def get_magic_resistance(self, magic_attack_type: MagicAttackType):
        if magic_attack_type == MagicAttackType.FIRE:
            return self.fire_resistance
        if magic_attack_type == MagicAttackType.ICE:
            return self.ice_resistance
        if magic_attack_type == MagicAttackType.SHOCK:
            return self.shock_resistance


class Strategy:

    def __init__(self, moves):
        self.current_move = -1
        self.moves_loop = moves

    def make_move(self):
        if self.current_move + 1 < len(self.moves_loop):
            self.current_move += 1
        else:
            self.current_move = 0
        return self.moves_loop[self.current_move]


class Creature:
    def __init__(self, health_points=100, strength=20,
                 power=20, armor=10, agility=10, magic_resistance=MagicResistance(), magic_attack_type=None):
        self.health_points = health_points
        self.strength = strength
        self.power = power
        self.armor = armor
        self.agility = agility
        self.magic_resistance = magic_resistance
        self.magic_attack_type = magic_attack_type

    def calculate_attack(self):
        return self.strength

    def calculate_armor(self):
        return self.armor

    def calculate_power(self):
        return self.power

    def receive_injuries(self, damage: int):
        self.health_points -= damage
        print("that much healt i have: ",self.health_points)

    def is_dead(self):
        return self.health_points <= 0

    def attack(self, attack_type):
        if attack_type == "Attack":
            return self.calculate_attack(), None
        else:
            print("thjis is magic modefaka mag typ", self.get_magic_attack_type())
            return self.calculate_power(), self.get_magic_attack_type()

    def reduce_damage(self, attack_type, damage, magic_attack_type):
        if attack_type == "Attack":
            return max(0, damage - self.calculate_armor())
        else:
            if self.magic_resistance is not None:
                print(magic_attack_type)
                return damage * (1 - self.magic_resistance.get_magic_resistance(magic_attack_type))
            else:
                return damage

    def get_magic_attack_type(self):
        return self.magic_attack_type

    def reset_creature_stats(self):
        self.health_points = 100



class Hero(Creature):

    def __init__(self, health_points=100, mana_points=100, strength=55,
                 power=10, armor=10, agility=10):
        Creature.__init__(self, health_points, strength, power, armor, agility)
        self.mana_points = mana_points
        self.gold = 10000
        self.active_sword: Sword = None
        self.active_armor: Armor = None
        self.active_wand: Wand = None
        self.active_potion: Potion = None
        self.items = init_inventory() # przedmioty gracza wszystkie inicjalizujemy na None

    def calculate_attack(self):
        if self.active_sword is not None:
            print("miecz huju")
            return self.strength + self.active_sword.strength_bonus
        else:
            print("tylko huju")
            return self.strength

    def calculate_armor(self):
        if self.active_armor is not None:
            return self.armor + self.active_armor.armor_bonus
        else:
            return self.armor

    def calculate_power(self):
        if self.active_wand is not None:
            print("rozdzka dziala")
            return self.power + self.active_wand.power_bonus
        else:
            return self.power

    def get_magic_attack_type(self):
        print("gttiung magic type")
        return self.active_wand.magic_type

    # TODO chyba trzeba zrobić że uzycie poty zabiera staminę plus zrobić żeby nie mozna było dwa razy poty użyć w walce
    def use_potion(self):
        if self.active_potion is not None:
            self.active_potion.heal_hero(self)

    def wear(self, item_name):
        item_o = self.items[item_name]
        if item_o is None:
            print("you don't own this item")
            return 1
        else:
            type = item_o.item_type
            if type == ItemType.SWORD:
                if self.active_sword == item_o:
                    return 2
                self.active_sword = item_o
                print("no chyba zalozyl")
            elif type == ItemType.WAND:
                if self.active_wand == item_o:
                    return 2
                self.active_wand = item_o
            elif type == ItemType.ARMOR:
                if self.active_armor == item_o:
                    return 2
                self.active_armor = item_o
            elif type == ItemType.POTION:
                if self.active_potion == item_o:
                    return 2
                self.active_potion = item_o
            else:
                print("gupi error którego pewnie nigdy nie będzie")
                return 3
            return 0

    def reset_creature_stats(self):
        Creature.reset_creature_stats(self)
        self.mana_points = 100




class Enemy(Creature):

    def __init__(self, image, health_points=100, strength=15,
                 power=10, armor=10, agility=10, magic_resistance=None, magic_attack_type=None, strategy=None):
        Creature.__init__(self, health_points, strength, power, armor, agility, magic_resistance, magic_attack_type)
        self.image = image
        self.magic_attack_type = magic_attack_type
        self.strategy = strategy