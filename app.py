from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Assure-toi d'avoir un fichier templates/index.html

@app.route('/jeux')
def jeux():
    return render_template('jeu.html')

@app.route('/consoles')
def consoles():
    return render_template('consolex.html')

@app.route('/entreprises')
def entreprises():
    return render_template('entreprises.html')

if __name__ == "__main__":
    app.run(debug=True)