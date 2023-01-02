import random

from flask import Flask
from flask import render_template
from flask import request
from characters import Skater, Longboarder, Rollerblader
from items import Potion1, Potion2, Potion3, Backpack
from actions import use_potion
from enemies import Enemy

app = Flask(__name__)


class Game:
    def __init__(self):
        pass


class Player:
    def __init__(self, name='Anonim', character_class=''):
        self.name = name
        self.character_class = character_class
        self.max_health = 1000
        self.health = 177
        self.strength = 0
        self.dexterity = 0
        self.charisma = 0
        self.damage1 = 0
        self.damage2 = 0
        self.attack_speed = 0
        self.critical_attack = 0

class Battle:
    def __init__(self):
        self.turn = 1

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
    classes = ['Deskorolkarz', 'Longboardzista', 'Rolkarz']
    return render_template('choose_class.htm', classes=classes, name=player.name)


@app.route('/stats', methods=['GET', 'POST'])
def show_stats():
    global player
    if request.method == 'POST':
        player.character_class = request.form.get('character_class')
    if player.character_class == 'Deskorolkarz':
        character = Skater()
    if player.character_class == 'Longboardzista':
        character = Longboarder()
    if player.character_class == 'Rolkarz':
        character = Rollerblader()

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

    global enemy
    enemy = Enemy()
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
                player.backpack.potion3 -= 1
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
    if enemy.health <= 0:
        return render_template('exit_battle_win.htm')

    if request.method == 'POST':
        if player.health > 0 and enemy.health > 0:
            action = request.form.get('action')
            if action == 'attack':
                enemy.health -= random.randint(player.damage1, player.damage2)
                player.health -= enemy.attack
                battle.turn += 1
            if request.form.get('potion') == 'potion1':
                if player.backpack.potion1 > 0:
                    potion = Potion1()
                    use_potion(player, potion)
                    player.backpack.potion1 -= 1
                    player.health -= enemy.attack
                    battle.turn += 1
            if request.form.get('potion') == 'potion2':
                if player.backpack.potion2 > 0:
                    potion = Potion2()
                    use_potion(player, potion)
                    player.backpack.potion3 -= 1
                    player.health -= enemy.attack
                    battle.turn += 1
            if request.form.get('potion') == 'potion3':
                if player.backpack.potion3 > 0:
                    potion = Potion3()
                    use_potion(player, potion)
                    player.backpack.potion3 -= 1
                    player.health -= enemy.attack
                    battle.turn += 1

    return render_template('battle.htm', backpack=player.backpack, enemy=enemy, player=player, battle=battle, potions=potions)


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5115, debug=True)



