from flask import Flask, render_template, request, jsonify
import csv
import os
import math
import random

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "prenom.csv")
COMPTEUR_PATH = os.path.join(os.path.dirname(__file__), "compteur.txt")

prenoms = {}
genres_dict = {}

def charger_prenoms():
    global prenoms, genres_dict
    prenoms = {}
    genre_raw = {}
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            prenom = row['preusuel'].strip().lower()
            if prenom.startswith('_'):
                continue
            try:
                nombre = int(row['nombre'])
                sexe = int(row['sexe'])
            except:
                continue
            if prenom not in prenoms:
                prenoms[prenom] = 0
                genre_raw[prenom] = set()
            prenoms[prenom] += nombre
            if sexe == 1:
                genre_raw[prenom].add('M')
            elif sexe == 2:
                genre_raw[prenom].add('F')
    # On a pour chaque prénom un set: {"M"}, {"F"} ou {"M", "F"}
    genres_dict = {k: v for k, v in genre_raw.items()}

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
    genre_set = genres_dict.get(prenom, set())
    genre_code = "U"
    if genre_set == {"M"}:
        genre_code = "M"
    elif genre_set == {"F"}:
        genre_code = "F"
    elif genre_set == {"M", "F"}:
        genre_code = "X"
    else:
        genre_code = "U"

    if freq == 0:
        prix = valeur_max
    else:
        logfreq = math.log(freq + 1)
        logmax = math.log(FREQ_MAX + 1)
        base = valeur_max * (1 - (logfreq / logmax))

        # BOOSTS ENORMES pour blazes pas chers, plus doux au-dessus
        if base < 50:
            bonus_court = max(0, 7 - n_lettres) * 18
            bonus_voyelles = n_voyelles * 10
            malus_consonnes = n_consonnes * -6
            boost_rare = n_rares * 24
        elif base < 100:
            bonus_court = max(0, 7 - n_lettres) * 5
            bonus_voyelles = n_voyelles * 2.5
            malus_consonnes = n_consonnes * -1.5
            boost_rare = n_rares * 8
        elif base < 150:
            bonus_court = max(0, 7 - n_lettres) * 2
            bonus_voyelles = n_voyelles * 1
            malus_consonnes = n_consonnes * -0.5
            boost_rare = n_rares * 2.5
        else:
            bonus_court = max(0, 7 - n_lettres) * 0.7
            bonus_voyelles = n_voyelles * 0.3
            malus_consonnes = n_consonnes * -0.12
            boost_rare = n_rares * 1

        bonus_tiret = 10 if is_tiret else 0

        prix = base + bonus_court + bonus_voyelles + malus_consonnes + boost_rare + bonus_tiret
        prix += random.uniform(-4, 7)
    prix = min(valeur_max, max(valeur_min, round(prix, 2)))

    # On retourne aussi le "genre" trouvé
    return jsonify({
        "prix": prix,
        "popularite": freq,
        "lettres": n_lettres,
        "voyelles": n_voyelles,
        "consonnes": n_consonnes,
        "lettres_rares": n_rares,
        "bonus_tiret": is_tiret,
        "genre": genre_code
    })

# ------ ZIGZIG API : calcul 0 à 20 + phrase mdr et image associée ------
@app.route('/api/zigzig')
def zigzig():
    prenom = request.args.get("prenom", "").strip().lower()
    genre = request.args.get("genre", "M")  # "M", "F", "X"
    n_lettres = len(prenom)
    n_voyelles, n_consonnes = compter_voyelles_consonnes(prenom)
    n_rares = compter_lettres_rares(prenom)
    # Algo "folklorique" :
    score = 5
    score += max(0, n_lettres - 4) * 1.5
    score += n_voyelles * 0.8
    score += n_consonnes * 1.1
    score += n_rares * 3.5
    if "-" in prenom or "'" in prenom:
        score += 1.5
    score += random.uniform(-2, 2)
    score = int(max(0, min(20, round(score))))

    # Phrase et image selon genre et score :
    if genre == "F":
        phrases = [
            "❄️ Franchement, tu zigzig jamais, c'est clean.",
            "😇 Sage, t'as même peur d'un bisou.",
            "🍯 Tu fais rêver les darons, mais c'est tout.",
            "👸 Classe, tu fais tourner les têtes, mais c'est discret.",
            "😏 Discrète mais efficace, tu zigzig à ta façon.",
            "💋 Tu fais des ravages au bal du quartier.",
            "💄 Toujours apprêtée, tu laisses pas indifférent.",
            "🌹 Les mecs sont à genoux, normal.",
            "🔥 T'es une vraie tentatrice, ça commence à chauffer.",
            "💃 T’es la reine des soirées, tout le monde veut ton 06.",
            "🥵 Les gars du quartier parlent que de toi.",
            "💍 On veut tous t'épouser, wallah.",
            "🚗 T’as déjà brisé 5 cœurs, y a la queue au kebab.",
            "🍑 Toi t'es la daronne de la zigzig.",
            "🚨 La BAC surveille tes moves, c'est chaud.",
            "🦄 T’es unique, tu zigzig à l’international.",
            "🍾 T’as déjà des groupies, même sur LinkedIn.",
            "💃 Le quartier s'enflamme à chaque fois que tu passes.",
            "🏆 Même Rocco te respecte, ça en dit long.",
            "👑 Queen, t’as level max, tout le monde veut te gérer."
        ]
        images = [
            "unicorn", "fun-emoji", "personas", "pixel-art", "adventurer", "micah", "croodles", "miniavs",
            "rings", "notionists", "thumbs", "big-ears", "adventurer-neutral", "bottts", "shapes"
        ]
    elif genre == "M":
        phrases = [
            "😇 Frérot, tu zigzig jamais, t’es en mode abstinent.",
            "🥚 Niveau 0, t’es pur comme l’eau de source.",
            "😴 Toujours solo, le néant total.",
            "🧢 Zarma tu dragues, mais ça prend pas.",
            "😬 T’as eu des dates… sur Candy Crush.",
            "👦 Le seul truc que t’as pécho c’est la grippe.",
            "🕵️‍♂️ Discret, mais un peu de taff reste à faire.",
            "🐱 T’es soft, tu grattes un bisou tous les 2 ans.",
            "😏 La street te repère, tu montes en puissance.",
            "🚦 Ça commence à swiper sur ton blaze.",
            "💪 Déjà t’as pécho à la fête du kebab, solide.",
            "🔥 Ça chauffe, tu passes au next level.",
            "💸 Tu gères, les meufs sortent le chéquier.",
            "🏎️ Tu fais des tours dans la city, les regards suivent.",
            "💯 Validé par les rebeus et les daronnes.",
            "👑 Les meufs du quartier font la queue.",
            "🦾 Niveau boss, tu zigzig à volonté.",
            "🚨 Arrête, c’est dangereux là, tu fais trembler le 93.",
            "🦍 Niveau Rocco Siffredi, le king du zigzig.",
            "🌋 H24, tu fais plaisir à toutes les femmes, même la voisine de 60 piges."
        ]
        images = [
            "bottts", "pixel-art", "rings", "big-ears", "miniavs", "adventurer", "micah", "shapes",
            "personas", "croodles", "fun-emoji", "adventurer-neutral", "notionists", "thumbs"
        ]
    else:
        phrases = [
            "😳 On sait pas trop, tu zigzig à ta sauce, tu choisis qui tu veux.",
            "🤡 Prénom mystère, le zigzig c’est selon l’humeur.",
            "🦄 Ambivalent, t’es inclassable, c’est freestyle.",
            "💣 T’es là pour tout le monde, partage c’est la base.",
            "🎭 Chameleon, tu zigzig tout le monde, personne safe.",
            "👽 Tu zigzig en secret, on a pas les stats.",
            "🍻 T’es open, tous les genres y passent.",
            "🎲 C’est random, comme ta vie sentimentale.",
            "🧬 Le zigzig n’a pas de sexe, toi non plus.",
            "🌀 T’es le bug de la matrice du zigzig.",
            "👁 Tu séduis même les robots, c’est fort.",
            "🦾 Polyvalent, tu te prives de rien.",
            "🌈 Arlequin du love, t’es en roue libre.",
            "⚡️ T’es une légende des deux côtés.",
            "🚁 Même la NASA te cherche.",
            "🛸 OVNI du zigzig, on sait pas te classer.",
            "🐍 Caméléon, t’adaptes selon le terrain.",
            "🥇 Polyzig, y a pas de limites.",
            "📛 T’es le badge universel du zigzig.",
            "👑 Masterclass universelle du zigzig !"
        ]
        images = [
            "croodles", "miniavs", "rings", "personas", "notionists", "fun-emoji", "pixel-art", "shapes", "adventurer-neutral"
        ]
    phrase = phrases[min(score, len(phrases) - 1)]
    avatar = images[score % len(images)]
    # url de l’avatar marrant pour le score de zigzig
    url = f"https://api.dicebear.com/7.x/{avatar}/svg?seed=zigzig{score}{prenom}"
    return jsonify({
        "score": score,
        "phrase": phrase,
        "avatar": url
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
