from flask import Flask, render_template, request
from models import db, Game

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Assure-toi d'avoir un fichier templates/index.html

@app.route('/jeux')
def jeux():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    pagination = Game.query.paginate(page=page, per_page=per_page)
    return render_template('jeux.html', games=pagination.items, pagination=pagination)

@app.route('/consoles')
def consoles():
    return render_template('consolex.html')

@app.route('/entreprises')
def entreprises():
    return render_template('entreprises.html')
