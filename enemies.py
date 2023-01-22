class Rabbit:
    def __init__(self):
        self.enemy_name = 'Królik'
        self.line = 1
        self.max_health = 300
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 10
        self.damage2 = 15
        self.attack_speed = 1
        self.critical_attack = 0.1

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2


class Boar:
    def __init__(self):
        self.enemy_name = 'Dzik'
        self.line = 2
        self.max_health = 450
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 25
        self.damage2 = 35
        self.attack_speed = 2
        self.critical_attack = 0.1

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2
class Deer:
    def __init__(self):
        self.enemy_name = 'Jeleń'
        self.line = 2
        self.max_health = 600
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 30
        self.damage2 = 40
        self.attack_speed = 1
        self.critical_attack = 0.1

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2


class Troll:
    def __init__(self):
        self.enemy_name = 'Troll'
        self.line = 3
        self.max_health = 800
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 60
        self.damage2 = 80
        self.attack_speed = 1
        self.critical_attack = 0.06

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2
class Goblin:
    def __init__(self):
        self.enemy_name = 'Goblin'
        self.line = 3
        self.max_health = 500
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 30
        self.damage2 = 40
        self.attack_speed = 4
        self.critical_attack = 0.06

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2


class Orc:
    def __init__(self):
        self.enemy_name = 'Ork'
        self.line = 3
        self.max_health = 750
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 50
        self.damage2 = 70
        self.attack_speed = 2
        self.critical_attack = 0.06

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2


class Dragon:
    def __init__(self):
        self.enemy_name = 'Smok'
        self.line = 4
        self.max_health = 1200
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.damage1 = 60
        self.damage2 = 80
        self.attack_speed = 3
        self.critical_attack = 0.06

    def strengthen(self):
        self.max_health *= 1.2
        self.damage1 *= 1.2
        self.damage2 *= 1.2

