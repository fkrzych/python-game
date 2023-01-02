class Skater:
    def __init__(self, damage1=2, damage2=3, attack_speed=2, critical_attack=0.2, dodge=0.2, block=0.2):
        self.strength = 10
        self.dexterity = 15
        self.charisma = 20
        self.damage1 = damage1 * self.strength
        self.damage2 = damage2 * self.strength
        self.attack_speed = attack_speed * self.dexterity
        self.critical_attack = "{:.1%}".format(critical_attack * self.charisma/100)
        self.block = "{:.1%}".format(block * self.strength/100)
        self.dodge = "{:.1%}".format(dodge * self.dexterity/100)

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma, self.attack_speed, self.critical_attack


class Longboarder:
    def __init__(self, damage1=2, damage2=3, attack_speed=2, critical_attack=0.2, dodge=0.2, block=0.2):
        self.strength = 20
        self.dexterity = 10
        self.charisma = 15
        self.damage1 = damage1 * self.strength
        self.damage2 = damage2 * self.strength
        self.attack_speed = attack_speed * self.dexterity
        self.critical_attack = "{:.1%}".format(critical_attack * self.charisma/100)
        self.block = "{:.1%}".format(block * self.strength / 100)
        self.dodge = "{:.1%}".format(dodge * self.dexterity / 100)

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma, self.attack_speed, self.critical_attack


class Rollerblader:
    def __init__(self, damage1=2, damage2=3, attack_speed=2, critical_attack=0.2, dodge=0.2, block=0.2):
        self.strength = 10
        self.dexterity = 20
        self.charisma = 15
        self.damage1 = damage1 * self.strength
        self.damage2 = damage2 * self.strength
        self.attack_speed = attack_speed * self.dexterity
        self.critical_attack = "{:.1%}".format(critical_attack * self.charisma/100)
        self.block = "{:.1%}".format(block * self.strength / 100)
        self.dodge = "{:.1%}".format(dodge * self.dexterity / 100)

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma, self.attack_speed, self.critical_attack

