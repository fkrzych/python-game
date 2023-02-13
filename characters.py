class OneHand:
    def __init__(self, damage1=2, damage2=3, attack_speed=2, critical_attack=0.6, dodge=0, block=1.2):
        self.strength = 10
        self.dexterity = 15
        self.charisma = 20
        self.damage1 = damage1 * self.strength
        self.damage2 = damage2 * self.strength
        self.attack_speed = attack_speed * self.dexterity / 10
        self.critical_attack = critical_attack * self.charisma/100
        self.block = block * self.strength / 100
        self.dodge = dodge * self.dexterity / 100

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma, self.attack_speed, self.critical_attack


class TwoHand:
    def __init__(self, damage1=2, damage2=3, attack_speed=2, critical_attack=0.6, dodge=0, block=0):
        self.strength = 20
        self.dexterity = 10
        self.charisma = 15
        self.damage1 = damage1 * self.strength
        self.damage2 = damage2 * self.strength
        self.attack_speed = attack_speed * self.dexterity / 10
        self.critical_attack = critical_attack * self.charisma/100
        self.block = block * self.strength / 100
        self.dodge = dodge * self.dexterity / 100

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma, self.attack_speed, self.critical_attack


class Daggers:
    def __init__(self, damage1=2, damage2=3, attack_speed=2, critical_attack=0.6, dodge=0.6, block=0):
        self.strength = 10
        self.dexterity = 20
        self.charisma = 15
        self.damage1 = damage1 * self.strength
        self.damage2 = damage2 * self.strength
        self.attack_speed = attack_speed * self.dexterity / 10
        self.critical_attack = critical_attack * self.charisma/100
        self.block = block * self.strength / 100
        self.dodge = dodge * self.dexterity / 100

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma, self.attack_speed, self.critical_attack

