from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Ne crée pas l'app Flask ici, juste l'objet db
db = SQLAlchemy()

# Table d'association pour relation many-to-many
# Jeux et langues
game_language = db.Table('language_supports',
                         db.Column('game_id', db.Integer,
                                   db.ForeignKey('game.id')),
                         db.Column('language_id', db.Integer,
                                   db.ForeignKey('language.id')),
                         db.Column('language_support_type_id', db.Integer,
                                   db.ForeignKey('language_supports_type.id'))
                         )

# Jeux et genres
game_genre = db.Table('game_genre',
                      db.Column('game_id', db.Integer,
                                db.ForeignKey('game.id')),
                      db.Column('genre_id', db.Integer,
                                db.ForeignKey('genres.id'))
                      )

# Game type et game
game_game_type = db.Table('game_game_type',
                          db.Column('game_id', db.Integer,
                                    db.ForeignKey('game.id')),
                          db.Column('category_id', db.Integer,
                                    db.ForeignKey('game_type.id'))
                          )

# Player perspectives et game
player_perspective = db.Table('game_player_perspective',
                              db.Column('game_id', db.Integer,
                                        db.ForeignKey('game.id')),
                              db.Column('perspective_id', db.Integer,
                                        db.ForeignKey('player_perspective.id'))
                              )

# Age ratings et game
age_rating = db.Table('game_age_rating',
                      db.Column('game_id', db.Integer,
                                db.ForeignKey('game.id')),
                      db.Column('age_rating_id', db.Integer,
                                db.ForeignKey('age_ratings.id'))
                      )

# Game multiplayer mode
game_multiplayer_mode = db.Table('game_multiplayer_mode',
                                 db.Column('game_id', db.Integer,
                                           db.ForeignKey('game.id')),
                                 db.Column('multiplayer_mode_id', db.Integer,
                                           db.ForeignKey('multiplayer_modes.id'))
                                 )

# Platform Multiplayer Mode
platform_multiplayer_mode = db.Table('platform_multiplayer_mode',
                                     db.Column('platform_id', db.Integer,
                                               db.ForeignKey('platform.id')),
                                     db.Column('multiplayer_mode_id', db.Integer,
                                               db.ForeignKey('multiplayer_modes.id'))
                                     )

# Platform Platform Version
platform_platform_version = db.Table('platform_platform_version',
                                     db.Column('platform_id', db.Integer,
                                               db.ForeignKey('platform.id')),
                                     db.Column('version_id', db.Integer,
                                               db.ForeignKey('platform_version.id'))
                                     )

# Game Game Engine
game_game_engine = db.Table('game_game_engine',
                            db.Column('game_id', db.Integer,
                                      db.ForeignKey('game.id')),
                            db.Column('engine_id', db.Integer,
                                      db.ForeignKey('game_engines.id'))
                            )

# Game Engine Logo
game_engine_logo = db.Table('game_engine_logo',
                            db.Column('engine_id', db.Integer,
                                      db.ForeignKey('game_engines.id')),
                            db.Column('logo_id', db.Integer,
                                      db.ForeignKey('game_engine_logos.id'))
                            )

# Company Game Engine
company_game_engine = db.Table('company_game_engine',
                               db.Column('company_id', db.Integer,
                                         db.ForeignKey('company.id')),
                               db.Column('engine_id', db.Integer,
                                         db.ForeignKey('game_engines.id'))
                               )

# Company Company Status
company_company_status = db.Table('company_company_status',
                                  db.Column('company_id', db.Integer,
                                            db.ForeignKey('company.id')),
                                  db.Column('status_id', db.Integer,
                                            db.ForeignKey('company_status.id'))
                                  )

# Company Company Logos
company_company_logos = db.Table('company_company_logos',
                                 db.Column('company_id', db.Integer,
                                           db.ForeignKey('company.id')),
                                 db.Column('logo_id', db.Integer,
                                           db.ForeignKey('company_logos.id'))
                                 )

# Company Developed By
company_developed_by = db.Table('company_developed_by',
                                db.Column('company_id', db.Integer,
                                          db.ForeignKey('company.id')),
                                db.Column('developer_id', db.Integer,
                                          db.ForeignKey('company.id'))
                                )

# Company Published By
company_published_by = db.Table('company_published_by',
                                db.Column('company_id', db.Integer,
                                          db.ForeignKey('company.id')),
                                db.Column('publisher_id', db.Integer,
                                          db.ForeignKey('company.id'))
                                )

# Modèles
# Game


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    summary = db.Column(db.Text)
    first_release_date = db.Column(db.Date)
    total_rating = db.Column(db.Float(5, 2))

    # Relation many-to-many
    # Langues
    languages = db.relationship('Language',
                                secondary=game_language,
                                backref=db.backref('games', lazy='dynamic'))

    # Genres
    genres = db.relationship('Genre',
                             secondary=game_genre,
                             backref=db.backref('games', lazy='dynamic'))

    # Type
    game_types = db.relationship('GameType',
                                 secondary=game_game_type,
                                 backref=db.backref('games', lazy='dynamic'))

    # Player Perspectives
    player_perspectives = db.relationship('PlayerPerspective',
                                          secondary=player_perspective,
                                          backref=db.backref('games', lazy='dynamic'))

    # Age Ratings
    age_ratings = db.relationship('AgeRating',
                                  secondary=age_rating,
                                  backref=db.backref('games', lazy='dynamic'))

    # Multiplayer Mode
    multiplayer_modes = db.relationship('MultiplayerMode',
                                        secondary=game_multiplayer_mode,
                                        backref=db.backref('games', lazy='dynamic'))

    game_engines = db.relationship('GameEngine',
                                   secondary=game_game_engine,
                                   backref=db.backref('games', lazy='dynamic'))

    def __repr__(self):
        return f"<Game {self.name}>"

# Language


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    locale = db.Column(db.String(100))
    name = db.Column(db.String(250))
    native_name = db.Column(db.String(250))

    def __repr__(self):
        return f"<Language {self.name}>"

# LanguageSupportsType


class LanguageSupportsType(db.Model):
    __tablename__ = 'language_supports_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<LanguageSupportType {self.name}>"

# Genre


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Genre {self.name}>"

# Videos Jeux


class GameVideo(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    video_id = db.Column(db.String(150))
    name = db.Column(db.String(200))

    game = db.relationship('Game', backref=db.backref('videos', lazy=True))

    def __repr__(self):
        return f"<GameVideo {self.name}>"


# Game Type
class GameType(db.Model):
    __tablename__ = 'game_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<GameType {self.name}>"


# Player Perspective
class PlayerPerspective(db.Model):
    __tablename__ = 'player_perspective'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __repr__(self):
        return f"<PlayerPerspective {self.name}>"


# Age rating
class AgeRating(db.Model):
    __tablename__ = 'age_ratings'
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(100))
    age = db.Column(db.String(100))

    def __repr__(self):
        return f"<AgeRating {self.organization} - {self.age}>"


# Multiplayer Modes
class MultiplayerMode(db.Model):
    __tablename__ = 'multiplayer_modes'
    id = db.Column(db.Integer, primary_key=True)
    campaingcoop = db.Column(db.Integer)         # tinyint(1)
    lancoop = db.Column(db.Integer)              # tinyint(1)
    offlinecoop = db.Column(db.Integer)          # tinyint(1)
    offlinecoopmax = db.Column(db.SmallInteger)  # smallint(6)
    onlinecoop = db.Column(db.Integer)           # tinyint(1)
    onlinecoopmax = db.Column(db.SmallInteger)   # smallint(6)
    onlinemax = db.Column(db.SmallInteger)       # smallint(6)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    splitscreen = db.Column(db.Integer)          # tinyint(1)
    splitscreenonline = db.Column(db.Integer)    # tinyint(1)

    def __repr__(self):
        return f"<MultiplayerMode {self.id}>"


# Platform
class Platform(db.Model):
    __tablename__ = 'platform'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    abbreviation = db.Column(db.String(50))
    summary = db.Column(db.Text)
    slug = db.Column(db.String(100))
    generation = db.Column(db.Integer)
    family = db.Column(db.String(100))
    type = db.Column(db.String(100))
    alternative_name = db.Column(db.String(250))

    # Relation many-to-many
    multiplayer_modes = db.relationship('MultiplayerMode',
                                        secondary=platform_multiplayer_mode,
                                        backref=db.backref('platforms', lazy='dynamic'))

    platform_version = db.relationship('PlatformVersion',
                                       secondary=platform_platform_version,
                                       backref=db.backref('platforms', lazy='dynamic'))

    def __repr__(self):
        return f"<Platform {self.name}>"


# Platform Version
class PlatformVersion(db.Model):
    __tablename__ = 'platform_version'
    id = db.Column(db.Integer, primary_key=True)
    version_name = db.Column(db.String(50))

    def __repr__(self):
        return f"<PlatformVersion {self.version_name}>"


# Game Engine
class GameEngine(db.Model):
    __tablename__ = 'game_engines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    slug = db.Column(db.String(150))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<GameEngine {self.name}>"

# Game Engine Logos


class GameEngineLogo(db.Model):
    __tablename__ = 'game_engine_logos'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

    game_engine = db.relationship('GameEngine',
                                  secondary=game_engine_logo,
                                  backref=db.backref('logos', lazy=True))

    def __repr__(self):
        return f"<GameEngineLogo {self.url}>"

# Company


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    changed_company_id = db.Column(db.Integer)
    country = db.Column(db.String(250))
    description = db.Column(db.Text)
    name = db.Column(db.String(150))
    parent = db.Column(db.Integer, db.ForeignKey('company.id'))
    slug = db.Column(db.String(150))
    start_date = db.Column(db.Date)
    status_id = db.Column(db.Integer)

    # Relation many-to-many
    game_engines = db.relationship('GameEngine',
                                   secondary=company_game_engine,
                                   backref=db.backref('companies', lazy='dynamic'))
    company_status = db.relationship('CompanyStatus',
                                     secondary=company_company_status,
                                     backref=db.backref('companies', lazy='dynamic'))
    company_logos = db.relationship('CompanyLogos',
                                    secondary=company_company_logos,
                                    backref=db.backref('companies', lazy='dynamic'))
    developed_by = db.relationship('Company',
                                   secondary=company_developed_by,
                                   primaryjoin=id == company_developed_by.c.company_id,
                                   secondaryjoin=id == company_developed_by.c.developer_id,
                                   backref=db.backref('developed_companies', lazy='dynamic'))
    published_by = db.relationship('Company',
                                   secondary=company_published_by,
                                   primaryjoin=id == company_published_by.c.company_id,
                                   secondaryjoin=id == company_published_by.c.publisher_id,
                                   backref=db.backref('published_companies', lazy='dynamic'))

    def __repr__(self):
        return f"<Company {self.name}>"

# Company Status


class CompanyStatus(db.Model):
    __tablename__ = 'company_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<CompanyStatus {self.name}>"

# Company Logos


class CompanyLogos(db.Model):
    __tablename__ = 'company_logos'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

    def __repr__(self):
        return f"<CompanyLogo {self.url}>"
