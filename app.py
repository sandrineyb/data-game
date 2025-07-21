from flask import Flask, redirect, render_template, request, url_for
from models import db, Game, Platform, Company
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from recommendation import recommend_games
import pycountry


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


# FOnction code ISO pays
def get_country_name(iso_code):
    if not iso_code:
        return ""
    country = pycountry.countries.get(alpha_2=iso_code.upper())
    return country.name if country else iso_code


# Gestionnaires d'erreurs globaux


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error("Page non trouvée: %s", str(e))
    return render_template('erreur.html',
                           message="Page non trouvée.",
                           error="L'URL demandée n'existe pas sur ce serveur."), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error("Erreur serveur interne: %s", str(e))
    return render_template('erreur.html',
                           message="Une erreur interne s'est produite.",
                           error=str(e)), 500


@app.errorhandler(Exception)
def handle_exception(e):
    # Pour toutes les autres exceptions non gérées
    app.logger.error("Exception non gérée: %s", str(e), exc_info=True)
    return render_template('erreur.html',
                           message="Une erreur inattendue s'est produite.",
                           error=str(e)), 500

# Routes


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/jeux')
def jeux():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    app.logger.debug("Récupération des jeux page %s", page)
    pagination = Game.query.paginate(page=page, per_page=per_page)
    return render_template('jeux.html', games=pagination.items, pagination=pagination)


@app.route('/consoles')
def consoles():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    app.logger.debug("Récupération des consoles page %s", page)
    pagination = Platform.query.paginate(page=page, per_page=per_page)
    return render_template('consoles.html', platforms=pagination.items, pagination=pagination)


@app.route('/entreprises')
def entreprises():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    app.logger.debug("Récupération des Entreprises page %s", page)
    pagination = Company.query.paginate(page=page, per_page=per_page)
    return render_template('entreprises.html', companies=pagination.items, pagination=pagination)


@app.route('/jeu/<slug>')
def jeu_detail(slug):
    game = Game.query.filter_by(slug=slug).first_or_404()
    # Obtenir les noms de jeux recommandés
    recommended_names = recommend_games(game.name, n=5)

    # Récupérer les objets Game depuis la base SQL
    recommandations = Game.query.filter(Game.name.in_(recommended_names)).all()

    return render_template('jeu_detail.html', game=game, recommandations=recommandations) 

@app.route('/console/<slug>')
def console_detail(slug):
    platform = Platform.query.filter_by(slug=slug).first_or_404()
    return render_template('platform_detail.html', platform=platform)

@app.route('/entreprise/<slug>')
def entreprise_detail(slug):
    company = Company.query.filter_by(slug=slug).first_or_404()
    return render_template('entreprises_detail.html', company=company, get_country_name=get_country_name)


@app.route('/rechercher')
def rechercher():
    query = request.args.get('q', '')

    if not query:
        return redirect(url_for('jeux'))

    resultats = Game.query.filter(
        Game.name.like(f'%{query}%')
    ).all()

    # Convertir les dates si nécessaire
    for jeu in resultats:
        if isinstance(jeu.first_release_date, str):
            try:
                # Supposant que le format est YYYY-MM-DD
                jeu.first_release_date = datetime.strptime(
                    jeu.first_release_date, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                # Gardez-le tel quel si la conversion échoue
                pass

    return render_template('resultats_recherche.html',
                           query=query,
                           resultats=resultats)


# Pour exécuter l'app en local
if __name__ == '__main__':
    app.run(debug=True)
