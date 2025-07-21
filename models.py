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
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'))
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
