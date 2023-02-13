import uuid
import math

from flask import Flask, redirect
from flask import render_template
from flask import session

from flask import request

from characters import OneHand, TwoHand, Daggers
from items import Potion1, Potion2, Potion3, Backpack
from actions import use_potion, calculate_attack, calculate_block, regenerate_energy, enemy_attacks, calculate_strong_attack, calculate_loot, calculate_dodge
from enemies import Rabbit, Boar, Deer, Troll, Goblin, Orc, Dragon

app = Flask(__name__)
app.secret_key = 'fgdgerwsg5eS'

games = {}
pvp_battles = {}
hotseats = {}


class Game:
    def __init__(self):
        self.line1_done = False
        self.line2_done = False
        self.line3_done = False
        self.line4_done = False
        self.turn = 0
        self.player = 0
        self.player_backpack = 0
        self.enemies = {}
        self.players = 0


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
        self.start_points = 10
        self.start_strength = 0
        self.start_dexterity = 0
        self.start_charisma = 0


class PvpBattle:
    def __init__(self, name):
        self.turn = 0
        self.name = name
        self.end = False
        self.start = False
        self.whose_turn = 0
        self.players = []
        self.active_player = 0

    def add_player(self):
        if self.start == False:
            self.player2 = ()
            return 1
        else:
            return -1

    def start_game(self):
        self.start = True


class Hotseat:
    def __init__(self):
        self.turn = 0
        self.end = False
        self.start = False
        self.whose_turn = 0
        # self.players = []
        self.player1 = 0
        self.player2 = 0

@app.route('/', methods=['GET', 'POST'])
def start_game():
    if 'key' not in session:
        session['key'] = uuid.uuid4()

    if request.method == 'POST':
        return choose_class()
    return render_template('start_game.htm')


def check_simple():
    if session.get('key') and 'games' in globals():
        return True
    return False


@app.route('/choose_class', methods=['GET', 'POST'])
def choose_class():
    if not check_simple():
        return redirect('/', code=302)

    games[session['key']] = Game()

    games[session['key']].enemies['rabbit'] = Rabbit()
    games[session['key']].enemies['boar'] = Boar()
    games[session['key']].enemies['deer'] = Deer()
    games[session['key']].enemies['troll'] = Troll()
    games[session['key']].enemies['goblin'] = Goblin()
    games[session['key']].enemies['orc'] = Orc()
    games[session['key']].enemies['dragon'] = Dragon()

    games[session['key']].player = Player()
    games[session['key']].player_backpack = Backpack()

    games[session['key']].player.name = request.form.get('character_name')
    classes = ['Broń jednoręczna i tarcza', 'Broń dwuręczna', 'Sztylety']
    weapons = ['OneHand', 'TwoHand', 'Daggers']
    return render_template('choose_class.htm', classes=classes, name=games[session['key']].player.name, weapons=weapons)


@app.route('/stats', methods=['GET', 'POST'])
def show_stats():
    if not check_simple():
        return redirect('/', code=302)

    if request.method == 'POST':
        games[session['key']].player.character_class = request.form.get('character_class')
        if games[session['key']].player.character_class == 'Broń jednoręczna i tarcza':
            character = OneHand()
        elif games[session['key']].player.character_class == 'Broń dwuręczna':
            character = TwoHand()
        elif games[session['key']].player.character_class == 'Sztylety':
            character = Daggers()

    games[session['key']].player.strength = character.strength
    games[session['key']].player.dexterity = character.dexterity
    games[session['key']].player.charisma = character.charisma
    games[session['key']].player.start_strength = character.strength
    games[session['key']].player.start_dexterity = character.dexterity
    games[session['key']].player.start_charisma = character.charisma
    games[session['key']].player.damage1 = character.damage1
    games[session['key']].player.damage2 = character.damage2
    games[session['key']].player.attack_speed = character.attack_speed
    games[session['key']].player.critical_attack = character.critical_attack
    games[session['key']].player.block = character.block
    games[session['key']].player.dodge = character.dodge

    stats_names = ['Siła', 'Zręczność', 'Charyzma', 'Obrażenia', 'Szybkość ataku', 'Cios krytyczny', 'Blok', 'Unik']
    return render_template('stats.htm', stats_names=stats_names, player=games[session['key']].player)


@app.route('/add_stats', methods=['GET', 'POST'])
def add_stats():
    if not check_simple():
        return redirect('/', code=302)

    if request.method == 'POST':
        add_stat = request.form.get('add_stat')
        sub_stat = request.form.get('sub_stat')

        if add_stat == 'strength1' and games[session['key']].player.start_points > 0:
            games[session['key']].player.strength += 1
            games[session['key']].player.damage1 += 2
            games[session['key']].player.damage2 += 2
            games[session['key']].player.start_points -= 1
        elif add_stat == 'strength3' and games[session['key']].player.start_points > 2:
            games[session['key']].player.strength += 3
            games[session['key']].player.damage1 += 2 * 3
            games[session['key']].player.damage2 += 2 * 3
            games[session['key']].player.start_points -= 3

        elif add_stat == 'dexterity1' and games[session['key']].player.start_points > 0:
            dexterity = 1
            games[session['key']].player.dexterity += dexterity
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Broń jednoręczna i tarcza':
                games[session['key']].player.dodge += dexterity / 250
            games[session['key']].player.attack_speed += 0.2
            games[session['key']].player.attack_speed = round(games[session['key']].player.attack_speed, 2)
            games[session['key']].player.start_points -= 1
        elif add_stat == 'dexterity3' and games[session['key']].player.start_points > 2:
            dexterity = 3
            games[session['key']].player.dexterity += dexterity
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Broń jednoręczna i tarcza':
                games[session['key']].player.dodge += dexterity / 250
            games[session['key']].player.attack_speed += 0.2 * 3
            games[session['key']].player.attack_speed = round(games[session['key']].player.attack_speed, 2)
            games[session['key']].player.start_points -= 3

        elif add_stat == 'charisma1' and games[session['key']].player.start_points > 0:
            charisma = 1
            games[session['key']].player.charisma += charisma
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Sztylety':
                games[session['key']].player.block += charisma / 250
            games[session['key']].player.critical_attack += charisma / 250
            games[session['key']].player.start_points -= 1
        elif add_stat == 'charisma3' and games[session['key']].player.start_points > 2:
            charisma = 3
            games[session['key']].player.charisma += charisma
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Sztylety':
                games[session['key']].player.block += charisma / 250
            games[session['key']].player.critical_attack += charisma / 250
            games[session['key']].player.start_points -= 3

        if sub_stat == 'strength1' and games[session['key']].player.start_points < 10 and games[
            session['key']].player.strength > games[session['key']].player.start_strength:
            games[session['key']].player.strength -= 1
            games[session['key']].player.damage1 -= 2
            games[session['key']].player.damage2 -= 2
            games[session['key']].player.start_points += 1
        elif sub_stat == 'strength3' and games[session['key']].player.start_points < 8 and games[
            session['key']].player.strength > games[session['key']].player.start_strength:
            games[session['key']].player.strength -= 3
            games[session['key']].player.damage1 -= 2 * 3
            games[session['key']].player.damage2 -= 2 * 3
            games[session['key']].player.start_points += 3

        elif sub_stat == 'dexterity1' and games[session['key']].player.start_points < 10 and games[
            session['key']].player.dexterity > games[session['key']].player.start_dexterity:
            dexterity = 1
            games[session['key']].player.dexterity -= dexterity
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Broń jednoręczna i tarcza':
                games[session['key']].player.dodge -= dexterity / 250
            games[session['key']].player.attack_speed -= 0.2
            games[session['key']].player.attack_speed = round(games[session['key']].player.attack_speed, 2)
            games[session['key']].player.start_points += 1
        elif sub_stat == 'dexterity3' and games[session['key']].player.start_points < 8 and games[
            session['key']].player.dexterity > games[session['key']].player.start_dexterity:
            dexterity = 3
            games[session['key']].player.dexterity -= dexterity
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Broń jednoręczna i tarcza':
                games[session['key']].player.dodge -= dexterity / 250
            games[session['key']].player.attack_speed -= 0.2 * 3
            games[session['key']].player.attack_speed = round(games[session['key']].player.attack_speed, 2)
            games[session['key']].player.start_points += 3

        elif sub_stat == 'charisma1' and games[session['key']].player.start_points < 10 and games[
            session['key']].player.charisma > games[session['key']].player.start_charisma:
            charisma = 1
            games[session['key']].player.charisma -= charisma
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Sztylety':
                games[session['key']].player.block -= charisma / 250
            games[session['key']].player.critical_attack -= charisma / 250
            games[session['key']].player.start_points += 1
        elif sub_stat == 'charisma3' and games[session['key']].player.start_points < 8 and games[
            session['key']].player.charisma > games[session['key']].player.start_charisma:
            charisma = 3
            games[session['key']].player.charisma -= charisma
            if games[session['key']].player.character_class != 'Broń dwuręczna' and games[
                session['key']].player.character_class != 'Sztylety':
                games[session['key']].player.block -= charisma / 250
            games[session['key']].player.critical_attack -= charisma / 250
            games[session['key']].player.start_points += 3

    stats_names = ['Siła', 'Zręczność', 'Charyzma', 'Obrażenia', 'Szybkość ataku', 'Cios krytyczny', 'Blok', 'Unik']
    return render_template('add_stats.htm', stats_names=stats_names, player=games[session['key']].player)


@app.route('/game', methods=['GET', 'POST'])
def game():
    if not check_simple():
        return redirect('/', code=302)

    potions = [Potion1(), Potion2(), Potion3()]

    games[session['key']].player.energy = games[session['key']].player.max_energy
    if games[session['key']].player.health < 0:
        games[session['key']].player.health = 1


    if request.method == 'POST':
        if request.form.get('potion') == 'potion1':
            if games[session['key']].player_backpack.potion1 > 0:
                potion = Potion1()
                use_potion(games[session['key']].player, potion)
                games[session['key']].player_backpack.potion1 -= 1
        if request.form.get('potion') == 'potion2':
            if games[session['key']].player_backpack.potion2 > 0:
                potion = Potion2()
                use_potion(games[session['key']].player, potion)
                games[session['key']].player_backpack.potion2 -= 1
        if request.form.get('potion') == 'potion3':
            if games[session['key']].player_backpack.potion3 > 0:
                potion = Potion3()
                use_potion(games[session['key']].player, potion)
                games[session['key']].player_backpack.potion3 -= 1

    enemies = ['rabbit', 'boar', 'deer', 'troll', 'goblin', 'orc', 'dragon']
    stats_names = ['Siła', 'Zręczność', 'Charyzma', 'Obrażenia', 'Szybkość ataku', 'Cios krytyczny', 'Blok', 'Unik']
    return render_template('game.htm', player=games[session['key']].player,
                           backpack=games[session['key']].player_backpack, potions=potions, stats_names=stats_names,
                           enemies=enemies)


@app.route('/game/battle', methods=['GET', 'POST'])
def battle():
    if not check_simple():
        return redirect('/', code=302)

    global enemy1

    if games[session['key']].line4_done:
        games[session['key']].line1_done = False
        games[session['key']].line2_done = False
        games[session['key']].line3_done = False
        games[session['key']].line4_done = False

    if request.method == 'POST':
        if request.form.get('enemy') == 'rabbit':
            enemy1 = games[session['key']].enemies['rabbit']
        elif request.form.get('enemy') == 'boar':
            if games[session['key']].line1_done:
                enemy1 = games[session['key']].enemies['boar']
            else:
                return render_template('cannot_fight.htm')
        elif request.form.get('enemy') == 'deer':
            if games[session['key']].line1_done:
                enemy1 = games[session['key']].enemies['deer']
            else:
                return render_template('cannot_fight.htm')
        elif request.form.get('enemy') == 'troll':
            if games[session['key']].line2_done:
                enemy1 = games[session['key']].enemies['troll']
            else:
                return render_template('cannot_fight.htm')
        elif request.form.get('enemy') == 'goblin':
            if games[session['key']].line2_done:
                enemy1 = games[session['key']].enemies['goblin']
            else:
                return render_template('cannot_fight.htm')
        elif request.form.get('enemy') == 'orc':
            if games[session['key']].line2_done:
                enemy1 = games[session['key']].enemies['orc']
            else:
                return render_template('cannot_fight.htm')
        elif request.form.get('enemy') == 'dragon':
            if games[session['key']].line3_done:
                enemy1 = games[session['key']].enemies['dragon']
            else:
                return render_template('cannot_fight.htm')

    if games[session['key']].player.health <= 0:
        return render_template('exit_battle_dead.htm')
    if enemy1.health <= 0:
        if enemy1.line == 1:
            games[session['key']].line1_done = True
        elif enemy1.line == 2:
            games[session['key']].line2_done = True
        elif enemy1.line == 3:
            games[session['key']].line3_done = True
        elif enemy1.line == 4:
            games[session['key']].line4_done = True

        enemy1.strengthen()
        enemy1.health = enemy1.max_health
        enemy1.energy = enemy1.max_energy
        calculate_loot(games[session['key']].player, games[session['key']].player_backpack, enemy1)
        games[session['key']].player.energy = games[session['key']].player.max_energy
        games[session['key']].turn = 0
        return render_template('exit_battle_win.htm', enemy1=enemy1)

    action = ''
    attack = 0
    attack_taken = 0
    is_critical = False
    is_critical_taken = False
    is_attack_taken_blocked = False
    is_attack_taken_dodged = False
    enemy_rests = False

    if request.method == 'POST':
        if games[session['key']].player.health > 0 and enemy1.health > 0:
            action = request.form.get('action')
            if action == 'attack' and games[session['key']].player.energy >= 10:
                attack, is_critical = calculate_attack(games[session['key']].player.damage1,
                                                       games[session['key']].player.damage2,
                                                       games[session['key']].player.critical_attack,
                                                       games[session['key']].player.attack_speed, is_critical)
                enemy1.health -= attack
                games[session['key']].player.energy -= 10

                attack_taken, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests = enemy_attacks(
                    enemy1, games[session['key']].player, is_critical_taken, is_attack_taken_blocked,
                    is_attack_taken_dodged, enemy_rests, attack_taken)

                games[session['key']].turn += 1
            elif action == 'strong_attack' and games[session['key']].player.energy >= 20:
                attack, is_critical = calculate_strong_attack(games[session['key']].player.damage1,
                                                              games[session['key']].player.damage2,
                                                              games[session['key']].player.critical_attack,
                                                              games[session['key']].player.attack_speed, is_critical)
                enemy1.health -= attack
                games[session['key']].player.energy -= 20

                attack_taken, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests = enemy_attacks(
                    enemy1, games[session['key']].player, is_critical_taken, is_attack_taken_blocked,
                    is_attack_taken_dodged, enemy_rests, attack_taken)

                games[session['key']].turn += 1

            if action == 'rest':

                if games[session['key']].player.energy < 100:
                    regenerate_energy(games[session['key']].player, 20)

                attack_taken, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests = enemy_attacks(
                    enemy1, games[session['key']].player, is_critical_taken, is_attack_taken_blocked,
                    is_attack_taken_dodged, enemy_rests, attack_taken)

                games[session['key']].turn += 1

    return render_template('battle.htm', backpack=games[session['key']].player_backpack, enemy1=enemy1,
                           player=games[session['key']].player, game=games[session['key']], attack=attack,
                           action=action, is_critical=is_critical, attack_taken=attack_taken,
                           is_critical_taken=is_critical_taken, is_attack_taken_blocked=is_attack_taken_blocked,
                           is_attack_taken_dodged=is_attack_taken_dodged, enemy_rests=enemy_rests,
                           enemy_name=enemy1.enemy_name)


@app.route('/game/pvp/create', methods=['GET', 'POST'])
def pvp():
    if not check_simple():
        return redirect('/', code=302)
    session['battle_uuid'] = str(uuid.uuid4())
    pvp_battles[session['battle_uuid']] = PvpBattle(games[session['key']].player.name)
    pvp_battles[session['battle_uuid']].players.append(games[session['key']].player)
    session['id'] = len(pvp_battles[session['battle_uuid']].players) - 1
    return redirect('/game/pvp/wait', code=302)


@app.route('/game/pvp/wait')
def wait():
    return render_template('wait.htm', game=pvp_battles[session['battle_uuid']])


@app.route('/game/pvp/rooms', methods=['GET', 'POST'])
def pvp_rooms():
    if not check_simple():
        return redirect('/', code=302)

    return render_template('pvp_rooms.htm', pvp_battles=pvp_battles)


@app.route('/game/pvp/form_join/<room>', methods=['GET', 'POST'])
def form_join(room):
    if request.method == 'POST':
        battle_uuid = request.form.getlist('room')[0]
        session['battle_uuid'] = battle_uuid
        pvp_battles[session['battle_uuid']].players.append(games[session['key']].player)
        session['id'] = len(pvp_battles[session['battle_uuid']].players)-1
        return redirect('/game/pvp/join', code=302)

    return render_template('form_join.htm', room=room)


@app.route('/game/pvp/join/')
def join():
    if pvp_battles[session['battle_uuid']].start == False:
        pvp_battles[session['battle_uuid']].start_game()
        return redirect('/game/pvp', code=302)

    return render_template('join.htm')


@app.route('/game/pvp', methods=['GET', 'POST'])
def pvp_fight():
    action = ''
    attack = 0
    attack_taken = 0
    is_critical = False
    is_critical_taken = False
    is_attack_taken_blocked = False
    is_attack_taken_dodged = False

    if request.method == 'POST' and pvp_battles[session['battle_uuid']].active_player%2 == session['id']:
        if pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].health > 0 and pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].health > 0:
            action = request.form.get('action')
            if action == 'attack' and pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].energy >= 10:
                attack, is_critical = calculate_attack(pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].damage1,
                                                       pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].damage2,
                                                       pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].critical_attack,
                                                       pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].attack_speed,
                                                       is_critical)

                if pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].block > 0:
                    is_attack_taken_blocked = calculate_block(pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].block, is_attack_taken_blocked)
                if pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].dodge > 0:
                    is_attack_taken_dodged = calculate_dodge(pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].dodge, is_attack_taken_blocked)
                if not (is_attack_taken_blocked or is_attack_taken_dodged):
                    pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].health -= attack

                # pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].health -= attack
                pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player)%2].energy -= 10

                pvp_battles[session['battle_uuid']].turn += 0.5
                pvp_battles[session['battle_uuid']].active_player += 1
            elif action == 'strong_attack' and pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].energy >= 20:
                attack, is_critical = calculate_strong_attack(pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player % 2].damage1,
                                                       pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player % 2].damage2,
                                                       pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player % 2].critical_attack,
                                                       pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player % 2].attack_speed,
                                                       is_critical)

                if pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].block > 0:
                    is_attack_taken_blocked = calculate_block(pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].block, is_attack_taken_blocked)
                if pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].dodge > 0:
                    is_attack_taken_dodged = calculate_dodge(pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].dodge, is_attack_taken_blocked)
                if not (is_attack_taken_blocked or is_attack_taken_dodged):
                    pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player+1)%2].health -= attack

                # pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player + 1) % 2].health -= attack
                pvp_battles[session['battle_uuid']].players[(pvp_battles[session['battle_uuid']].active_player) % 2].energy -= 20

                pvp_battles[session['battle_uuid']].turn += 0.5
                pvp_battles[session['battle_uuid']].active_player += 1

            if action == 'rest':
                if pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2].energy < 100:
                    regenerate_energy(pvp_battles[session['battle_uuid']].players[pvp_battles[session['battle_uuid']].active_player%2], 20)

                pvp_battles[session['battle_uuid']].turn += 0.5
                pvp_battles[session['battle_uuid']].active_player += 1
    elif request.method == 'POST' and pvp_battles[session['battle_uuid']].active_player%2 != session['id']:
        return render_template('not_your_turn.htm')
    return render_template('pvp_battle.htm', game=pvp_battles[session['battle_uuid']],
                           player1=pvp_battles[session['battle_uuid']].players[0],
                           player2=pvp_battles[session['battle_uuid']].players[1], attack=attack, action=action,
                           is_critical=is_critical, attack_taken=attack_taken, is_critical_taken=is_critical_taken,
                           is_attack_taken_blocked=is_attack_taken_blocked,
                           is_attack_taken_dodged=is_attack_taken_dodged, whose_turn=pvp_battles[session['battle_uuid']].whose_turn)


# HOT SEAT
@app.route('/start_hotseat', methods=['GET', 'POST'])
def start_hotseat():
    if not check_simple():
        return redirect('/', code=302)

    if request.method == 'POST':
        return choose_class_hotseat()

    return render_template('start_hotseat.htm')


@app.route('/choose_class_hotseat', methods=['GET', 'POST'])
def choose_class_hotseat():
    if not check_simple():
        return redirect('/', code=302)

    hotseats[session['key']] = Hotseat()

    hotseats[session['key']].player1 = Player()
    hotseats[session['key']].player2 = Player()

    hotseats[session['key']].player1.name = request.form.get('character_name1')
    hotseats[session['key']].player2.name = request.form.get('character_name2')

    classes = ['Broń jednoręczna i tarcza', 'Broń dwuręczna', 'Sztylety']
    weapons = ['OneHand', 'TwoHand', 'Daggers']

    return render_template('choose_class_hotseat.htm', classes=classes, hotseat=hotseats[session['key']], weapons=weapons)


@app.route('/stats_hotseat', methods=['GET', 'POST'])
def show_stats_hotseat():
    global character2, character1
    if not check_simple():
        return redirect('/', code=302)

    if request.method == 'POST':
        hotseats[session['key']].player1.character_class = request.form.get('character_class1')
        hotseats[session['key']].player2.character_class = request.form.get('character_class2')

    if hotseats[session['key']].player1.character_class == 'Broń jednoręczna i tarcza':
        character1 = OneHand()
    elif hotseats[session['key']].player1.character_class == 'Broń dwuręczna':
        character1 = TwoHand()
    elif hotseats[session['key']].player1.character_class == 'Sztylety':
        character1 = Daggers()

    if hotseats[session['key']].player2.character_class == 'Broń jednoręczna i tarcza':
        character2 = OneHand()
    elif hotseats[session['key']].player2.character_class == 'Broń dwuręczna':
        character2 = TwoHand()
    elif hotseats[session['key']].player2.character_class == 'Sztylety':
        character2 = Daggers()

    hotseats[session['key']].player1.strength = character1.strength
    hotseats[session['key']].player1.dexterity = character1.dexterity
    hotseats[session['key']].player1.charisma = character1.charisma
    hotseats[session['key']].player1.start_strength = character1.strength
    hotseats[session['key']].player1.start_dexterity = character1.dexterity
    hotseats[session['key']].player1.start_charisma = character1.charisma
    hotseats[session['key']].player1.damage1 = character1.damage1
    hotseats[session['key']].player1.damage2 = character1.damage2
    hotseats[session['key']].player1.attack_speed = character1.attack_speed
    hotseats[session['key']].player1.critical_attack = character1.critical_attack
    hotseats[session['key']].player1.block = character1.block
    hotseats[session['key']].player1.dodge = character1.dodge

    hotseats[session['key']].player2.strength = character2.strength
    hotseats[session['key']].player2.dexterity = character2.dexterity
    hotseats[session['key']].player2.charisma = character2.charisma
    hotseats[session['key']].player2.start_strength = character2.strength
    hotseats[session['key']].player2.start_dexterity = character2.dexterity
    hotseats[session['key']].player2.start_charisma = character2.charisma
    hotseats[session['key']].player2.damage1 = character2.damage1
    hotseats[session['key']].player2.damage2 = character2.damage2
    hotseats[session['key']].player2.attack_speed = character2.attack_speed
    hotseats[session['key']].player2.critical_attack = character2.critical_attack
    hotseats[session['key']].player2.block = character2.block
    hotseats[session['key']].player2.dodge = character2.dodge


    stats_names = ['Siła', 'Zręczność', 'Charyzma', 'Obrażenia', 'Szybkość ataku', 'Cios krytyczny', 'Blok', 'Unik']
    return render_template('stats_hotseat.htm', stats_names=stats_names, hotseat=hotseats[session['key']])


@app.route('/add_stats_hotseat', methods=['GET', 'POST'])
def add_stats_hotseat():
    if not check_simple():
        return redirect('/', code=302)

    if request.method == 'POST':
        add_stat1 = request.form.get('add_stat1')
        sub_stat1 = request.form.get('sub_stat1')
        add_stat2 = request.form.get('add_stat2')
        sub_stat2 = request.form.get('sub_stat2')

        if add_stat1 == 'strength1' and hotseats[session['key']].player1.start_points > 0:
            hotseats[session['key']].player1.strength += 1
            hotseats[session['key']].player1.damage1 += 2
            hotseats[session['key']].player1.damage2 += 2
            hotseats[session['key']].player1.start_points -= 1
        elif add_stat1 == 'strength3' and hotseats[session['key']].player1.start_points > 2:
            hotseats[session['key']].player1.strength += 3
            hotseats[session['key']].player1.damage1 += 2 * 3
            hotseats[session['key']].player1.damage2 += 2 * 3
            hotseats[session['key']].player1.start_points -= 3

        elif add_stat1 == 'dexterity1' and hotseats[session['key']].player1.start_points > 0:
            dexterity = 1
            hotseats[session['key']].player1.dexterity += dexterity
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player1.dodge += dexterity / 250
            hotseats[session['key']].player1.attack_speed += 0.2
            hotseats[session['key']].player1.attack_speed = round(hotseats[session['key']].player1.attack_speed, 2)
            hotseats[session['key']].player1.start_points -= 1
        elif add_stat1 == 'dexterity3' and hotseats[session['key']].player1.start_points > 2:
            dexterity = 3
            hotseats[session['key']].player1.dexterity += dexterity
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player1.dodge += dexterity / 250
            hotseats[session['key']].player1.attack_speed += 0.2 * 3
            hotseats[session['key']].player1.attack_speed = round(hotseats[session['key']].player1.attack_speed, 2)
            hotseats[session['key']].player1.start_points -= 3

        elif add_stat1 == 'charisma1' and hotseats[session['key']].player1.start_points > 0:
            charisma = 1
            hotseats[session['key']].player1.charisma += charisma
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Sztylety':
                hotseats[session['key']].player1.block += charisma / 250
            hotseats[session['key']].player1.critical_attack += charisma / 250
            hotseats[session['key']].player1.start_points -= 1
        elif add_stat1 == 'charisma3' and hotseats[session['key']].player1.start_points > 2:
            charisma = 3
            hotseats[session['key']].player1.charisma += charisma
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Sztylety':
                hotseats[session['key']].player1.block += charisma / 250
            hotseats[session['key']].player1.critical_attack += charisma / 250
            hotseats[session['key']].player1.start_points -= 3

        if sub_stat1 == 'strength1' and hotseats[session['key']].player1.start_points < 10 and hotseats[
            session['key']].player1.strength > hotseats[session['key']].player1.start_strength:
            hotseats[session['key']].player1.strength -= 1
            hotseats[session['key']].player1.damage1 -= 2
            hotseats[session['key']].player1.damage2 -= 2
            hotseats[session['key']].player1.start_points += 1
        elif sub_stat1 == 'strength3' and hotseats[session['key']].player1.start_points < 8 and hotseats[
            session['key']].player1.strength > hotseats[session['key']].player1.start_strength:
            hotseats[session['key']].player1.strength -= 3
            hotseats[session['key']].player1.damage1 -= 2 * 3
            hotseats[session['key']].player1.damage2 -= 2 * 3
            hotseats[session['key']].player1.start_points += 3

        elif sub_stat1 == 'dexterity1' and hotseats[session['key']].player1.start_points < 10 and hotseats[
            session['key']].player1.dexterity > hotseats[session['key']].player1.start_dexterity:
            dexterity = 1
            hotseats[session['key']].player1.dexterity -= dexterity
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player1.dodge -= dexterity / 250
            hotseats[session['key']].player1.attack_speed -= 0.2
            hotseats[session['key']].player1.attack_speed = round(hotseats[session['key']].player1.attack_speed, 2)
            hotseats[session['key']].player1.start_points += 1
        elif sub_stat1 == 'dexterity3' and hotseats[session['key']].player1.start_points < 8 and hotseats[
            session['key']].player1.dexterity > hotseats[session['key']].player1.start_dexterity:
            dexterity = 3
            hotseats[session['key']].player1.dexterity -= dexterity
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player1.dodge -= dexterity / 250
            hotseats[session['key']].player1.attack_speed -= 0.2 * 3
            hotseats[session['key']].player1.attack_speed = round(hotseats[session['key']].player1.attack_speed, 2)
            hotseats[session['key']].player1.start_points += 3

        elif sub_stat1 == 'charisma1' and hotseats[session['key']].player1.start_points < 10 and hotseats[
            session['key']].player1.charisma > hotseats[session['key']].player1.start_charisma:
            charisma = 1
            hotseats[session['key']].player1.charisma -= charisma
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Sztylety':
                hotseats[session['key']].player1.block -= charisma / 250
            hotseats[session['key']].player1.critical_attack -= charisma / 250
            hotseats[session['key']].player1.start_points += 1
        elif sub_stat1 == 'charisma3' and hotseats[session['key']].player1.start_points < 8 and hotseats[
            session['key']].player1.charisma > hotseats[session['key']].player1.start_charisma:
            charisma = 3
            hotseats[session['key']].player1.charisma -= charisma
            if hotseats[session['key']].player1.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player1.character_class != 'Sztylety':
                hotseats[session['key']].player1.block -= charisma / 250
            hotseats[session['key']].player1.critical_attack -= charisma / 250
            hotseats[session['key']].player1.start_points += 3

    #     PLAYER2
        if add_stat2 == 'strength1' and hotseats[session['key']].player2.start_points > 0:
            hotseats[session['key']].player2.strength += 1
            hotseats[session['key']].player2.damage1 += 2
            hotseats[session['key']].player2.damage2 += 2
            hotseats[session['key']].player2.start_points -= 1
        elif add_stat2 == 'strength3' and hotseats[session['key']].player2.start_points > 2:
            hotseats[session['key']].player2.strength += 3
            hotseats[session['key']].player2.damage1 += 2 * 3
            hotseats[session['key']].player2.damage2 += 2 * 3
            hotseats[session['key']].player2.start_points -= 3

        elif add_stat2 == 'dexterity1' and hotseats[session['key']].player2.start_points > 0:
            dexterity = 1
            hotseats[session['key']].player2.dexterity += dexterity
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player2.dodge += dexterity / 250
            hotseats[session['key']].player2.attack_speed += 0.2
            hotseats[session['key']].player2.attack_speed = round(hotseats[session['key']].player2.attack_speed, 2)
            hotseats[session['key']].player2.start_points -= 1
        elif add_stat2 == 'dexterity3' and hotseats[session['key']].player2.start_points > 2:
            dexterity = 3
            hotseats[session['key']].player2.dexterity += dexterity
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player2.dodge += dexterity / 250
            hotseats[session['key']].player2.attack_speed += 0.2 * 3
            hotseats[session['key']].player2.attack_speed = round(hotseats[session['key']].player2.attack_speed, 2)
            hotseats[session['key']].player2.start_points -= 3

        elif add_stat2 == 'charisma1' and hotseats[session['key']].player2.start_points > 0:
            charisma = 1
            hotseats[session['key']].player2.charisma += charisma
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Sztylety':
                hotseats[session['key']].player2.block += charisma / 250
            hotseats[session['key']].player2.critical_attack += charisma / 250
            hotseats[session['key']].player2.start_points -= 1
        elif add_stat2 == 'charisma3' and hotseats[session['key']].player2.start_points > 2:
            charisma = 3
            hotseats[session['key']].player2.charisma += charisma
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Sztylety':
                hotseats[session['key']].player2.block += charisma / 250
            hotseats[session['key']].player2.critical_attack += charisma / 250
            hotseats[session['key']].player2.start_points -= 3

        if sub_stat2 == 'strength1' and hotseats[session['key']].player2.start_points < 10 and hotseats[
            session['key']].player2.strength > hotseats[session['key']].player2.start_strength:
            hotseats[session['key']].player2.strength -= 1
            hotseats[session['key']].player2.damage1 -= 2
            hotseats[session['key']].player2.damage2 -= 2
            hotseats[session['key']].player2.start_points += 1
        elif sub_stat2 == 'strength3' and hotseats[session['key']].player2.start_points < 8 and hotseats[
            session['key']].player2.strength > hotseats[session['key']].player2.start_strength:
            hotseats[session['key']].player2.strength -= 3
            hotseats[session['key']].player2.damage1 -= 2 * 3
            hotseats[session['key']].player2.damage2 -= 2 * 3
            hotseats[session['key']].player2.start_points += 3

        elif sub_stat2 == 'dexterity1' and hotseats[session['key']].player2.start_points < 10 and hotseats[
            session['key']].player2.dexterity > hotseats[session['key']].player2.start_dexterity:
            dexterity = 1
            hotseats[session['key']].player2.dexterity -= dexterity
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player2.dodge -= dexterity / 250
            hotseats[session['key']].player2.attack_speed -= 0.2
            hotseats[session['key']].player2.attack_speed = round(hotseats[session['key']].player2.attack_speed, 2)
            hotseats[session['key']].player2.start_points += 1
        elif sub_stat2 == 'dexterity3' and hotseats[session['key']].player2.start_points < 8 and hotseats[
            session['key']].player2.dexterity > hotseats[session['key']].player2.start_dexterity:
            dexterity = 3
            hotseats[session['key']].player2.dexterity -= dexterity
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Broń jednoręczna i tarcza':
                hotseats[session['key']].player2.dodge -= dexterity / 250
            hotseats[session['key']].player2.attack_speed -= 0.2 * 3
            hotseats[session['key']].player2.attack_speed = round(hotseats[session['key']].player2.attack_speed, 2)
            hotseats[session['key']].player2.start_points += 3

        elif sub_stat2 == 'charisma1' and hotseats[session['key']].player2.start_points < 10 and hotseats[
            session['key']].player2.charisma > hotseats[session['key']].player2.start_charisma:
            charisma = 1
            hotseats[session['key']].player2.charisma -= charisma
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Sztylety':
                hotseats[session['key']].player2.block -= charisma / 250
            hotseats[session['key']].player2.critical_attack -= charisma / 250
            hotseats[session['key']].player2.start_points += 1
        elif sub_stat2 == 'charisma3' and hotseats[session['key']].player2.start_points < 8 and hotseats[
            session['key']].player2.charisma > hotseats[session['key']].player2.start_charisma:
            charisma = 3
            hotseats[session['key']].player2.charisma -= charisma
            if hotseats[session['key']].player2.character_class != 'Broń dwuręczna' and hotseats[
                session['key']].player2.character_class != 'Sztylety':
                hotseats[session['key']].player2.block -= charisma / 250
            hotseats[session['key']].player2.critical_attack -= charisma / 250
            hotseats[session['key']].player2.start_points += 3


    stats_names = ['Siła', 'Zręczność', 'Charyzma', 'Obrażenia', 'Szybkość ataku', 'Cios krytyczny', 'Blok', 'Unik']
    return render_template('add_stats_hotseat.htm', stats_names=stats_names, hotseat=hotseats[session['key']])


@app.route('/hotseat_battle', methods=['GET', 'POST'])
def hotseat_battle():
    action = ''
    attack = 0
    attack_taken = 0
    is_critical = False
    is_critical_taken = False
    is_attack_taken_blocked = False
    is_attack_taken_dodged = False

    if request.method == 'POST' and hotseats[session['key']].whose_turn%2 == 0:
        if hotseats[session['key']].player1.health > 0 and hotseats[session['key']].player2.health > 0:
            action = request.form.get('action')
            if action == 'attack' and hotseats[session['key']].player1.energy >= 10:
                attack, is_critical = calculate_attack(hotseats[session['key']].player1.damage1,
                                                       hotseats[session['key']].player1.damage2,
                                                       hotseats[session['key']].player1.critical_attack,
                                                       hotseats[session['key']].player1.attack_speed,
                                                       is_critical)

                if hotseats[session['key']].player2.block > 0:
                    is_attack_taken_blocked = calculate_block(hotseats[session['key']].player2.block, is_attack_taken_blocked)
                if hotseats[session['key']].player2.dodge > 0:
                    is_attack_taken_dodged = calculate_dodge(hotseats[session['key']].player2.dodge, is_attack_taken_blocked)
                if not (is_attack_taken_blocked or is_attack_taken_dodged):
                    hotseats[session['key']].player2.health -= attack


                # hotseats[session['key']].player2.health -= attack
                hotseats[session['key']].player1.energy -= 10

                hotseats[session['key']].turn += 0.5
                hotseats[session['key']].whose_turn += 1

            elif action == 'strong_attack' and hotseats[session['key']].player1.energy >= 10:
                attack, is_critical = calculate_strong_attack(hotseats[session['key']].player1.damage1,
                                                       hotseats[session['key']].player1.damage2,
                                                       hotseats[session['key']].player1.critical_attack,
                                                       hotseats[session['key']].player1.attack_speed,
                                                       is_critical)

                if hotseats[session['key']].player2.block > 0:
                    is_attack_taken_blocked = calculate_block(hotseats[session['key']].player2.block, is_attack_taken_blocked)
                if hotseats[session['key']].player2.dodge > 0:
                    is_attack_taken_dodged = calculate_dodge(hotseats[session['key']].player2.dodge, is_attack_taken_blocked)
                if not (is_attack_taken_blocked or is_attack_taken_dodged):
                    hotseats[session['key']].player2.health -= attack

                # hotseats[session['key']].player2.health -= attack
                hotseats[session['key']].player1.energy -= 20

                hotseats[session['key']].turn += 0.5
                hotseats[session['key']].whose_turn += 1

            elif action == 'rest':
                if hotseats[session['key']].player1.energy < 100:
                    regenerate_energy(hotseats[session['key']].player1, 20)

                hotseats[session['key']].turn += 0.5
                hotseats[session['key']].whose_turn += 1

    elif request.method == 'POST' and hotseats[session['key']].whose_turn%2 == 1:
        if hotseats[session['key']].player1.health > 0 and hotseats[session['key']].player2.health > 0:
            action = request.form.get('action')
            if action == 'attack' and hotseats[session['key']].player2.energy >= 10:
                attack, is_critical = calculate_attack(hotseats[session['key']].player2.damage1,
                                                       hotseats[session['key']].player2.damage2,
                                                       hotseats[session['key']].player2.critical_attack,
                                                       hotseats[session['key']].player2.attack_speed,
                                                       is_critical)

                if hotseats[session['key']].player1.block > 0:
                    is_attack_taken_blocked = calculate_block(hotseats[session['key']].player1.block, is_attack_taken_blocked)
                if hotseats[session['key']].player1.dodge > 0:
                    is_attack_taken_dodged = calculate_dodge(hotseats[session['key']].player1.dodge, is_attack_taken_blocked)
                if not (is_attack_taken_blocked or is_attack_taken_dodged):
                    hotseats[session['key']].player1.health -= attack

                # hotseats[session['key']].player1.health -= attack
                hotseats[session['key']].player2.energy -= 10

                hotseats[session['key']].turn += 0.5
                hotseats[session['key']].whose_turn += 1
            elif action == 'strong_attack' and hotseats[session['key']].player2.energy >= 10:
                attack, is_critical = calculate_strong_attack(hotseats[session['key']].player2.damage1,
                                                              hotseats[session['key']].player2.damage2,
                                                              hotseats[session['key']].player2.critical_attack,
                                                              hotseats[session['key']].player2.attack_speed,
                                                              is_critical)

                if hotseats[session['key']].player1.block > 0:
                    is_attack_taken_blocked = calculate_block(hotseats[session['key']].player1.block,
                                                              is_attack_taken_blocked)
                if hotseats[session['key']].player1.dodge > 0:
                    is_attack_taken_dodged = calculate_dodge(hotseats[session['key']].player1.dodge,
                                                             is_attack_taken_blocked)
                if not (is_attack_taken_blocked or is_attack_taken_dodged):
                    hotseats[session['key']].player1.health -= attack

                # hotseats[session['key']].player1.health -= attack
                hotseats[session['key']].player2.energy -= 20

                hotseats[session['key']].turn += 0.5
                hotseats[session['key']].whose_turn += 1

            elif action == 'rest':
                if hotseats[session['key']].player2.energy < 100:
                    regenerate_energy(hotseats[session['key']].player2, 20)

                hotseats[session['key']].turn += 0.5
                hotseats[session['key']].whose_turn += 1

    return render_template('hotseat_battle.htm', hotseat=hotseats[session['key']])


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5115, debug=True)
