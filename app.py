from boggle import Boggle
from flask import Flask, render_template,session, request, jsonify
boggle_game = Boggle()

app = Flask(__name__)
app.config["SECERT_KEY"] = "abc123"

@app.route("/")
def homepage():
    #show the board 

    board = boggle_game.make_board
    session["board"] = board
    highscore = session.get["highscore", 0]
    nplays = session.get["nplays", 0]

    return render_template("index.html")


@app.route("/check-word")
def check_word():
    #check word if it in dictionary 
    
    word = request.arg["word"]
    board = session.get["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({"result": response})

