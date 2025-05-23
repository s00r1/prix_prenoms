from flask import Flask, render_template, request, jsonify
import csv
import os
import math
import random

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "prenom.csv")
COMPTEUR_PATH = os.path.join(os.path.dirname(__file__), "compteur.txt")

prenoms = {}

def charger_prenoms():
    global prenoms
    prenoms = {}
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            prenom = row['preusuel'].strip().lower()
            if prenom.startswith('_'):
                continue
            try:
                nombre = int(row['nombre'])
            except:
                continue
            if prenom not in prenoms:
                prenoms[prenom] = 0
            prenoms[prenom] += nombre

charger_prenoms()
FREQ_MAX = max(prenoms.values())

def compter_voyelles_consonnes(prenom):
    voyelles = "aeiouy"
    n_voyelles = sum(1 for c in prenom if c in voyelles)
    n_consonnes = sum(1 for c in prenom if c.isalpha() and c not in voyelles)
    return n_voyelles, n_consonnes

def compter_lettres_rares(prenom):
    rares = set("wqzxkyjhç")
    return sum(1 for c in prenom if c in rares)

def lire_compteur():
    try:
        with open(COMPTEUR_PATH, "r") as f:
            return int(f.read())
    except:
        return 0

def incrementer_compteur():
    compteur = lire_compteur() + 1
    with open(COMPTEUR_PATH, "w") as f:
        f.write(str(compteur))
    return compteur

@app.route('/')
def index():
    compteur = incrementer_compteur()
    return render_template('index.html', compteur=compteur)

@app.route('/api/prix-prenom')
def prix_prenom():
    valeur_max = 200
    valeur_min = 10
    prenom = request.args.get("prenom", "").strip().lower()
    freq = prenoms.get(prenom, 0)
    n_lettres = len(prenom)
    n_voyelles, n_consonnes = compter_voyelles_consonnes(prenom)
    n_rares = compter_lettres_rares(prenom)
    is_tiret = '-' in prenom or "'" in prenom

    if freq == 0:
        prix = valeur_max
    else:
        logfreq = math.log(freq + 1)
        logmax = math.log(FREQ_MAX + 1)
        base = valeur_max * (1 - (logfreq / logmax))

        # PALIERS BOOST
        if base < 50:
            bonus_court = max(0, 7 - n_lettres) * 7
            bonus_voyelles = n_voyelles * 3
            malus_consonnes = n_consonnes * -4
            boost_rare = n_rares * 20
        elif base < 100:
            bonus_court = max(0, 7 - n_lettres) * 2.2
            bonus_voyelles = n_voyelles * 1.2
            malus_consonnes = n_consonnes * -1.5
            boost_rare = n_rares * 7
        elif base < 150:
            bonus_court = max(0, 7 - n_lettres) * 1
            bonus_voyelles = n_voyelles * 0.6
            malus_consonnes = n_consonnes * -0.8
            boost_rare = n_rares * 2.2
        else:
            bonus_court = max(0, 7 - n_lettres) * 0.4
            bonus_voyelles = n_voyelles * 0.2
            malus_consonnes = n_consonnes * -0.2
            boost_rare = n_rares * 0.8

        bonus_tiret = 10 if is_tiret else 0

        prix = base + bonus_court + bonus_voyelles + malus_consonnes + boost_rare + bonus_tiret
        prix += random.uniform(-5, 7)
    prix = min(valeur_max, max(valeur_min, round(prix, 2)))
    return jsonify({
        "prix": prix,
        "popularite": freq,
        "lettres": n_lettres,
        "voyelles": n_voyelles,
        "consonnes": n_consonnes,
        "lettres_rares": n_rares,
        "bonus_tiret": is_tiret
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
