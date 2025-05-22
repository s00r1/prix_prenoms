from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

# Chemin vers le fichier CSV INSEE
CSV_PATH = os.path.join(os.path.dirname(__file__), "prenom.csv")

prenoms = {}

# Charger le CSV une fois au démarrage
def charger_prenoms():
    global prenoms
    prenoms = {}
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            prenom = row['preusuel'].strip().lower()
            nombre = int(row['nombre'])
            if prenom not in prenoms:
                prenoms[prenom] = 0
            prenoms[prenom] += nombre

charger_prenoms()
FREQ_MAX = max(prenoms.values())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prix-prenom')
def prix_prenom():
    valeur_max = 200
    prenom = request.args.get("prenom", "").strip().lower()
    freq = prenoms.get(prenom, 0)
    if freq == 0:
        prix = valeur_max
    else:
        prix = valeur_max - (freq / FREQ_MAX) * valeur_max
    prix = max(0, round(prix, 2))
    return jsonify({"prix": prix, "popularite": freq})

if __name__ == "__main__":
    app.run(debug=True)
