from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

class Skater(): pass

class Longboarder(): pass

class Rollerblader(): pass


@app.route('/', methods=['GET', 'POST'])
def start_game():
    if request.method == 'POST':
        return 'OK'
    return render_template('start_game.htm')


@app.route('/choose_class')
def choose_class():
    global game
    game = Game()
    classes = ['Deskorolkarz', 'Longboardzista', 'Rolkarz']
    return render_template('choose_class.htm', classes=classes)


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5115, debug=True)


class Game():
    def __int__(self):
        self.player_name = ''
