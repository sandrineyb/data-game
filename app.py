from flask import Flask, render_template, request
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

# Pour exécuter l'app en local
if __name__ == '__main__':
    app.run(debug=True)
