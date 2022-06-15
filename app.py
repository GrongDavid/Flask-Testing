from crypt import methods
from boggle import Boggle
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "horsey90"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

boggle_game = Boggle()

@app.route('/')
def home_board():
    board = boggle_game.make_board()
    session['board'] = board
    score = session.get('score', 0)
    times_played = session.get('times_played', 0)
    return render_template('board.html', board=board, score=score, times_played=times_played)

@app.route('/word-check')
def word_check():
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)
    return jsonify({'response': res})

@app.route('/score', methods=['POST'])
def score():
    score = request.json['score']
    times_played = session.get('times_played')
    session['times_played'] = times_played + 1
    session['score'] = score
    return jsonify(score)

