from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)


class Game:
    def __init__(self, name='Anonim', character_class=''):
        self.player_name = name
        self.character_class = character_class


class Skater:
    def __init__(self):
        self.strength = 15
        self.dexterity = 10
        self.charisma = 10

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma


class Longboarder:
    def __init__(self):
        self.strength = 10
        self.dexterity = 15
        self.charisma = 10

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma


class Rollerblader:
    def __init__(self):
        self.strength = 10
        self.dexterity = 10
        self.charisma = 15

    def __repr__(self):
        return self.strength, self.dexterity, self.charisma


@app.route('/', methods=['GET', 'POST'])
def start_game():
    if request.method == 'POST':
        return choose_class()
    return render_template('start_game.htm')


@app.route('/choose_class', methods=['GET', 'POST'])
def choose_class():
    global game
    game = Game()
    game.player_name = request.form.get('character_name')
    classes = ['Deskorolkarz', 'Longboardzista', 'Rolkarz']
    return render_template('choose_class.htm', classes=classes, name=game.player_name)


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    global game
    if request.method == 'POST':
        game.character_class = request.form.get('character_class')
    if game.character_class == 'Deskorolkarz':
        character = Skater()
    if game.character_class == 'Longboardzista':
        character = Longboarder()
    if game.character_class == 'Rolkarz':
        character = Rollerblader()
    stats = character.__repr__()
    return render_template('stats.htm', name=game.player_name, character_class=game.character_class, stats=stats)


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5115, debug=True)



