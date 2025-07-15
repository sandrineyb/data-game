from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Charge les variables d'environnement du .env
load_dotenv()

app = Flask(__name__)

# Configuration SQLAlchemy avec pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('BDD_USER')}:{os.getenv('BDD_PSWD')}"
    f"@{os.getenv('BDD_HOST')}/{os.getenv('BDD_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
