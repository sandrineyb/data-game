from flask import Flask, redirect, render_template, request, url_for
from models import db, Game
from dotenv import load_dotenv
import os
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)

# Charge les variables d'environnement
load_dotenv()

# Crée l'app Flask
app = Flask(__name__)

# Configuration SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('BDD_USER')}:{os.getenv('BDD_PSWD')}"
    f"@{os.getenv('BDD_HOST')}/{os.getenv('BDD_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise db avec l'app
db.init_app(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # Assure-toi d'avoir un fichier templates/index.html

@app.route('/jeux')
def jeux():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 25
        app.logger.debug("Récupération des jeux page %s", page)
        pagination = Game.query.paginate(page=page, per_page=per_page)
        return render_template('jeux.html', games=pagination.items, pagination=pagination)
    except Exception as e:
        app.logger.error("Erreur dans la route /jeux : %s", str(e))
        return f"Erreur : {str(e)}", 500

@app.route('/consoles')
def consoles():
    return render_template('consoles.html')  # Corrigé la typo

@app.route('/entreprises')
def entreprises():
    return render_template('entreprises.html')

@app.route('/jeu/<slug>')
def jeu_detail(slug):
    game = Game.query.filter_by(slug=slug).first_or_404()
    return render_template('jeu_detail.html', game=game)

@app.route('/rechercher')
def rechercher():
    # Récupère le terme de recherche depuis l'URL
    query = request.args.get('q', '')
    
    # Si aucun terme n'est fourni, redirige vers la liste des jeux
    if not query:
        return redirect(url_for('jeux'))

    # Recherche dans la base de données (insensible à la casse)
    resultats = Game.query.filter(
        Game.name.ilike(f'%{query}%')
    ).all()
    
    # Affiche les résultats
    return render_template('resultats_recherche.html', 
                          query=query, 
                          resultats=resultats)

# Pour exécuter l'app en local
if __name__ == '__main__':
    app.run(debug=True)
