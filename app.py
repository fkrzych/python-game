from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

class Game():
    def __int__(self, name='Anonim'):
        self.player_name = name

class Skater(): pass

class Longboarder(): pass

class Rollerblader(): pass


@app.route('/', methods=['GET', 'POST'])
def start_game():
    if request.method == 'POST':
        return choose_class()
    return render_template('start_game.htm')


@app.route('/choose_class')
def choose_class():
    global game
    game = Game()
    game.player_name = request.form.get('character_name')
    classes = ['Deskorolkarz', 'Longboardzista', 'Rolkarz']
    return render_template('choose_class.htm', classes=classes, name=game.player_name)


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5115, debug=True)



