from flask import Flask, redirect, render_template, request, url_for
from models import db, Game, Platform, Company, Genre, GameEngine, GameEngineLogo, game_platform, game_genre, game_game_engine, company_game_engine, game_engine_logo
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from recommendation import recommend_games
from traductionpays import code_vers_nom_pays
from sqlalchemy.exc import OperationalError
from sqlalchemy import func


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
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True
}

# Initialise db avec l'app
db.init_app(app)


# Fonction code ISO pays
def get_country_name(iso_code):
    return code_vers_nom_pays(iso_code)


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


@app.errorhandler(OperationalError)
def handle_db_error(e):
    app.logger.error("Erreur base de données: %s", str(e))
    return render_template(
        'erreur.html',
        message="Erreur de connexion à la base de données.",
        error=str(e)
    ), 500

# Routes


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/jeux')
def jeux():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    selected_genres = request.args.getlist('genre', type=int)
    sort = request.args.get('sort', 'date_desc')
    date_min = request.args.get('date_min', type=int)
    date_max = request.args.get('date_max', type=int)

    query = Game.query

    # Filtre genres
    if selected_genres:
        query = query.join(game_genre, Game.id == game_genre.c.game_id) \
                     .join(Genre, Genre.id == game_genre.c.genre_id) \
                     .filter(Genre.id.in_(selected_genres))

    # Filtre dates
    if date_min:
        query = query.filter(Game.first_release_date >= f"{date_min}-01-01")
    if date_max:
        query = query.filter(Game.first_release_date <= f"{date_max}-12-31")

    # Tri par date
    if sort == 'date_asc':
        query = query.order_by(Game.first_release_date.asc())
    else:
        query = query.order_by(Game.first_release_date.desc())

    pagination = query.paginate(page=page, per_page=per_page)

    all_genres = Genre.query.order_by(Genre.name).all()

    return render_template(
        'jeux.html',
        games=pagination.items,
        pagination=pagination,
        all_genres=all_genres,
        selected_genres=selected_genres,
        selected_sort=sort,
        date_min=date_min,
        date_max=date_max,
        current_year=datetime.now().year
    )


@app.route('/consoles')
def consoles():
    page = request.args.get('page', 1, type=int)
    per_page = 25

    query = Platform.query

    selected_generation = request.args.get('generation', type=int)
    selected_family = request.args.get('family', type=str)

    if selected_generation:
        query = query.filter(Platform.generation == selected_generation)
    if selected_family:
        selected_family = selected_family.strip()
        query = query.filter(func.lower(
            func.trim(Platform.family)) == selected_family.lower())

    pagination = query.paginate(page=page, per_page=per_page)

    generations = db.session.query(
        Platform.generation).distinct().order_by(Platform.generation).all()
    families = [
        (fam[0].strip(),) for fam in db.session.query(Platform.family)
        .filter(Platform.family.isnot(None)).distinct().order_by(Platform.family).all()
    ]

    return render_template(
        'consoles.html',
        platforms=pagination.items,
        pagination=pagination,
        selected_generation=selected_generation,
        generations=generations,
        selected_family=selected_family,
        families=families
    )


@app.route('/entreprises')
def entreprises():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    app.logger.debug("Récupération des Entreprises page %s", page)
    pagination = Company.query.paginate(page=page, per_page=per_page)
    return render_template('entreprises.html', companies=pagination.items, pagination=pagination)

@app.route('/moteurs-graphique')
def engines():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    app.logger.debug("Récupération des Game engines page %s", page)
    pagination = GameEngine.query.paginate(page=page, per_page=per_page)
    return render_template('moteurs_graphique.html', engines=pagination.items, pagination=pagination)


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
    mode_max = {}
    for mode in platform.multiplayer_modes:
        for key, value in mode.__dict__.items():
            if key not in ['_sa_instance_state', 'id', 'platform_id'] and value and value != 0:
                # On garde la valeur maximale pour chaque clé
                if key not in mode_max or value > mode_max[key]:
                    mode_max[key] = value
    # Transforme en liste de tuples pour le template
    multiplayer_modes_display = list(mode_max.items())

    # Top 5 jeux les mieux notés pour la console
    top_5_games = Game.query.join(game_platform).filter(
        game_platform.c.platform_id == platform.id
    ).order_by(Game.total_rating.desc()).limit(5).all()

    return render_template(
        'console_detail.html',
        platform=platform,
        multiplayer_modes_display=multiplayer_modes_display,
        top_5_games=top_5_games
    )


@app.route('/entreprise/<slug>')
def entreprise_detail(slug):
    company = Company.query.filter_by(slug=slug).first_or_404()
    jeux_associes = Game.query \
        .join(game_game_engine).join(GameEngine) \
        .join(company_game_engine) \
        .filter(company_game_engine.c.company_id == company.id) \
        .all()
    
    return render_template('entreprises_detail.html', company=company, get_country_name=get_country_name, jeux_associes=jeux_associes)


@app.route('/moteur-graphique/<slug>')
def engines_detail(slug):
    engines = GameEngine.query.filter_by(slug=slug).first_or_404()
    
    return render_template('moteurs_graphique_detail.html', engines=engines)


@app.route('/rechercher')
def rechercher():
    try:
        query = request.args.get('q', '')
        if not query:
            return redirect(url_for('jeux'))

        # Recherche pour chaque catégorie
        jeux = Game.query.filter(Game.name.ilike(f'%{query}%')).limit(50).all()
        consoles = Platform.query.filter(Platform.name.ilike(f'%{query}%')).limit(50).all()
        entreprises = Company.query.filter(Company.name.ilike(f'%{query}%')).limit(50).all()
        engines = GameEngine.query.filter(GameEngine.name.ilike(f'%{query}%')).limit(50).all()

        # Convertir les dates si nécessaire
        for jeu in jeux:
            if isinstance(jeu.first_release_date, str):
                try:
                    jeu.first_release_date = datetime.strptime(
                        jeu.first_release_date, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass

        return render_template('resultats_recherche.html', query=query, jeux=jeux, consoles=consoles, entreprises=entreprises,  engines=engines, get_country_name=get_country_name)
    except Exception as e:
        app.logger.error("Erreur dans /rechercher: %s", str(e), exc_info=True)
        return render_template(
            'erreur.html',
            message="Une erreur est survenue lors de la recherche.",
            error=str(e)
        ), 500


# Pour exécuter l'app en local
if __name__ == '__main__':
    app.run(debug=True)
