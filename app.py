from flask import Flask
from flask import render_template
from flask import request
from characters import OneHand, TwoHand, Daggers
from items import Potion1, Potion2, Potion3, Backpack
from actions import use_potion, calculate_attack, calculate_block, regenerate_energy, enemy_attacks
from enemies import Enemy1

app = Flask(__name__)


class Game:
    def __init__(self):
        pass


class Player:
    def __init__(self, name='Anonim', character_class=''):
        self.name = name
        self.character_class = character_class
        self.max_health = 1000
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.strength = 0
        self.dexterity = 0
        self.charisma = 0
        self.damage1 = 0
        self.damage2 = 0
        self.attack_speed = 0
        self.critical_attack = 0


class Battle:
    def __init__(self):
        self.turn = 0


@app.route('/', methods=['GET', 'POST'])
def start_game():
    if request.method == 'POST':
        return choose_class()
    return render_template('start_game.htm')


@app.route('/choose_class', methods=['GET', 'POST'])
def choose_class():
    global player
    player = Player()
    player.backpack = Backpack()

    player.name = request.form.get('character_name')
    classes = ['Broń jednoręczna i tarcza', 'Broń dwuręczna', 'Sztylety']
    weapons = ['OneHand', 'TwoHand', 'Daggers']
    return render_template('choose_class.htm', classes=classes, name=player.name, weapons=weapons)


@app.route('/stats', methods=['GET', 'POST'])
def show_stats():
    global player
    if request.method == 'POST':
        player.character_class = request.form.get('character_class')
    if player.character_class == 'Broń jednoręczna i tarcza':
        character = OneHand()
    if player.character_class == 'Broń dwuręczna':
        character = TwoHand()
    if player.character_class == 'Sztylety':
        character = Daggers()

    player.strength = character.strength
    player.dexterity = character.dexterity
    player.charisma = character.charisma
    player.damage1 = character.damage1
    player.damage2 = character.damage2
    player.attack_speed = character.attack_speed
    player.critical_attack = character.critical_attack
    player.block = character.block
    player.dodge = character.dodge

    stats_names = ['Siła', 'Zręczność', 'Charyzma', 'Obrażenia', 'Szybkość ataku', 'Cios krytyczny', 'Blok', 'Unik']
    return render_template('stats.htm', stats_names=stats_names, player=player)


@app.route('/game', methods=['GET', 'POST'])
def game():
    global player
    potions = [Potion1(), Potion2(), Potion3()]

    global battle
    battle = Battle()

    global enemy1
    enemy1 = Enemy1()
    if request.method == 'POST':
        if request.form.get('potion') == 'potion1':
            if player.backpack.potion1 > 0:
                potion = Potion1()
                use_potion(player, potion)
                player.backpack.potion1 -= 1
        if request.form.get('potion') == 'potion2':
            if player.backpack.potion2 > 0:
                potion = Potion2()
                use_potion(player, potion)
                player.backpack.potion2 -= 1
        if request.form.get('potion') == 'potion3':
            if player.backpack.potion3 > 0:
                potion = Potion3()
                use_potion(player, potion)
                player.backpack.potion3 -= 1
    return render_template('game.htm', player=player, backpack=player.backpack, potions=potions)


@app.route('/game/battle', methods=['GET', 'POST'])
def battle():
    global player
    global battle
    potions = [Potion1(), Potion2(), Potion3()]

    if player.health <= 0:
        return render_template('exit_battle_dead.htm')
    if enemy1.health <= 0:
        player.energy = player.max_energy
        return render_template('exit_battle_win.htm')

    action = ''
    attack = 0
    attack_taken = 0
    is_critical = False
    is_critical_taken = False
    is_attack_taken_blocked = False
    is_attack_taken_dodged = False
    enemy_rests = False

    if request.method == 'POST':
        if player.health > 0 and enemy1.health > 0:
            action = request.form.get('action')
            if action == 'attack' and player.energy > 0:
                attack, is_critical = calculate_attack(player.damage1, player.damage2, player.critical_attack, player.attack_speed, is_critical)
                enemy1.health -= attack
                player.energy -= 10

                attack_taken, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests = enemy_attacks(enemy1, player, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests, attack_taken)

                battle.turn += 1
            elif action == 'attack' and player.energy <= 0:
                return 'Nie masz siły zaatakować!'
            if action == 'rest':

                if player.energy < 100:
                    regenerate_energy(player, 20)

                attack_taken, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests = enemy_attacks(enemy1, player, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests, attack_taken)

                battle.turn += 1

    return render_template('battle.htm', backpack=player.backpack, enemy1=enemy1, player=player, battle=battle, potions=potions, attack=attack, action=action, is_critical=is_critical, attack_taken=attack_taken, is_critical_taken=is_critical_taken, is_attack_taken_blocked=is_attack_taken_blocked, is_attack_taken_dodged=is_attack_taken_dodged, enemy_rests=enemy_rests)


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5115, debug=True)



