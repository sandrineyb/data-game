from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Assure-toi d'avoir un fichier templates/index.html

if __name__ == '__main__':
    app.run(debug=True)