from flask import Flask, render_template, request, jsonify
import csv
import os
import math
import random

app = Flask(__name__)

# Chemin vers le fichier CSV INSEE
CSV_PATH = os.path.join(os.path.dirname(__file__), "prenom.csv")

prenoms = {}

def charger_prenoms():
    global prenoms
    prenoms = {}
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            prenom = row['preusuel'].strip().lower()
            if prenom.startswith('_'):
                continue  # Ignore les "_PRENOMS_RARES"
            try:
                nombre = int(row['nombre'])
            except:
                continue
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
    valeur_min = 10  # prix plancher, aucun prénom sous 10€
    prenom = request.args.get("prenom", "").strip().lower()
    freq = prenoms.get(prenom, 0)
    if freq == 0:
        prix = valeur_max
    else:
        logfreq = math.log(freq + 1)
        logmax = math.log(FREQ_MAX + 1)
        prix = valeur_max * (1 - (logfreq / logmax))
        prix += random.uniform(-5, 5)  # un peu de street random
    prix = min(valeur_max, max(valeur_min, round(prix, 2)))
    return jsonify({"prix": prix, "popularite": freq})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
