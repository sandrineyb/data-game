from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Ne crée pas l'app Flask ici, juste l'objet db
db = SQLAlchemy()

# Modèle Game
class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    summary = db.Column(db.Text)
    first_release_date = db.Column(db.Date)
    total_rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Game {self.name}>"
