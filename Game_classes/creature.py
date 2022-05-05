from Game_classes.item import Sword, Armor, Wand, Potion
from enum import Enum
from Game_classes.item import init_inventory, ItemType

class Creature:
    def __init__(self, health_points=100, mana_points=100, stamina_points=100, strength=20,
                 power=20, armor=10, agility=10, knowledge=10, magic_resistance=None, magic_attack_type=None):
        self.health_points = health_points
        self.mana_points = mana_points # potrzebe tylko graczowi
        self.stamina_points = stamina_points
        self.strength = strength
        self.power = power
        self.armor = armor
        self.agility = agility
        self.knowledge = knowledge
        if magic_resistance is None:
            self.magic_resistance = MagicResistance()
        else:
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

    def is_dead(self):
        return self.health_points <= 0

    def attack(self, attacked_creature):
        stamina_cost = self.calculate_stamina_attack_cost()
        if stamina_cost <= self.stamina_points:
            attack = self.calculate_attack()
            attacked_creature_armor = attacked_creature.calculate_armor()
            attacked_creature.receive_injuries(attack - attacked_creature_armor)
            print(attack - attacked_creature_armor)
            self.stamina_points -= self.calculate_stamina_attack_cost()
            print("melee dupa")
            return True
        else:
            return False

    # TODO czy mana cost jest staly?
    def magic_attack(self, attacked_creature):
        if self.magic_attack_type is not None and self.mana_points >= 100:
            power = self.calculate_power()
            magic_resistance = self.magic_resistance.get_magic_resistance(self.get_magic_attack_type())
            damage = power * (1 - magic_resistance)
            attacked_creature.receive_injuries(damage)
            self.mana_points -= 100
            return True
        else:
            return False

    # TODO może trzeba dodać jakis limit energy
    def regenerate_stamina(self):
        self.stamina_points += self.agility

    def regenerate_mana(self):
        self.mana_points += 10

    def get_magic_attack_type(self):
        return self.magic_attack_type

    def calculate_stamina_attack_cost(self):
        return 10


class Hero(Creature):

    def __init__(self, health_points=100, mana_points=100, stamina_points=100, strength=20,
                 power=10, armor=10, agility=10, magic_resistance=None, magic_attack_type=None):
        Creature.__init__(self, health_points, mana_points, stamina_points, strength, power, armor, agility,
                          magic_resistance, magic_attack_type)
        self.gold = 100
        self.active_sword: Sword = None
        self.active_armor: Armor = None
        self.active_wand: Wand = None
        self.active_potion: Potion = None
        self.items = init_inventory() # przedmioty gracza wszystkie inicjalizujemy na None

    def calculate_attack(self):
        if self.active_sword is not None:
            return self.strength + self.active_sword.strength_bonus
        else:
            return self.strength

    def calculate_armor(self):
        if self.active_armor is not None:
            return self.armor + self.active_armor.armor_bonus
        else:
            return self.armor

    def calculate_power(self):
        if self.active_wand is not None:
            return self.power + self.active_wand.power_bonus
        else:
            return self.power

    def get_magic_attack_type(self):
        return self.active_wand.magic_type

    # TODO chyba trzeba zrobić że uzycie poty zabiera staminę plus zrobić żeby nie mozna było dwa razy poty użyć w walce
    def use_potion(self):
        if self.active_potion is not None:
            self.active_potion.heal_hero(self)

    # TODO moze bd jeszcze jakiś odpowiedzni dla bohatera stamina cost czy coś dla samej łapy
    def calculate_stamina_attack_cost(self):
        if self.active_sword is not None:
            return self.active_sword.attack_stamina_cost
        else:
            return 10

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


class Enemy(Creature):

    def __init__(self, health_points=100, mana_points=100, stamina_points=100, strength=15,
                 power=10, armor=10, agility=10, stamina_attack_cost = 10, magic_resistance=None, magic_attack_type=None):
        Creature.__init__(self, health_points, mana_points, stamina_points, strength, power, armor, agility,
                          magic_resistance, magic_attack_type)
        self.stamina_attack_cost = stamina_attack_cost
        self.strategy = Strategy()

    def calculate_stamina_attack_cost(self):
        return self.stamina_attack_cost

    def magic_attack(self, attacked_creature):
        if self.mana_points >= 100:
            power = self.calculate_power()
            # magic_resistance = self.magic_resistance.get_magic_resistance(self.get_magic_attack_type())
            # damage = power * (1 - magic_resistance)
            damage = power
            attacked_creature.receive_injuries(damage)
            self.mana_points -= 100
            return True
        else:
            return False


class MagicAttackType(Enum):
    FIRE = 1
    ICE = 2
    SHOCK = 3


class MagicResistance:

    def __init__(self, fire_resistance=0, ice_resistance=0, shock_resistance=0):
        self.fire_resistance = fire_resistance
        self.ice_resistance = ice_resistance
        self.shock_resistance = shock_resistance

    def get_magic_resistance(self, magic_attack_type: MagicAttackType):
        if (magic_attack_type == MagicAttackType.FIRE):
            return self.fire_resistance
        if (magic_attack_type == MagicAttackType.ICE):
            return self.ice_resistance
        if (magic_attack_type == MagicAttackType.SHOCK):
            return self.shock_resistance


class Strategy:

    def __init__(self):
        self.moves_loop = ["melee attack", "melee attack", "melee attack", "magic attack"]
        self.current_move = -1

    def make_move(self):
        if self.current_move + 1 < len(self.moves_loop):
            self.current_move += 1
        else:
            self.current_move = 0
        return self.moves_loop[self.current_move]
