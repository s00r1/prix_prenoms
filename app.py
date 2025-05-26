from flask import Flask, render_template, request, jsonify
import csv
import os
import math
import random
import json

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "prenom.csv")
COMPTEUR_PATH = os.path.join(os.path.dirname(__file__), "compteur.txt")
BLAZE_HITS_PATH = os.path.join(os.path.dirname(__file__), "blaze_hits.json")

prenoms = {}
genres_dict = {}

SURNOMS_STREET = [
    "La Menace", "Turbo", "Le Sang", "Le Chacal", "El Maestro", "La Rafale", "Big Mac", "Le Pigeon", "Le Fou", "La Boulette",
    "Grillav", "La Foudre", "El Gitan", "Bougnoule", "Don Kebab", "El Boulette", "Ratatouille", "El Poulet", "La Rafale", "Cobra",

    # ADDITIONS VIOLENTES
    "Le Michto", "Kalash Douceur", "P’tit Grillé", "MC Semoule", "La Tige", "Zinzin du 7-5", "Pépito", "Frérot Shlag", "Tonton Bicot",
    "Le Ténébreux du Lavomatic", "Le Daron Fantôme", "ChichaMan", "Le Détourneur", "DJ PLS", "El Barbier Fou", "Zébulon", "Zarma Flex",
    "Don Coucous", "Soso la Saucisse", "Captain Brochette", "Bastos Soft", "Yaya l’Errant", "Le Transpalette", "Tchico la Plage",
    "Chef d'Étage", "Le Zèbre", "Fils du Zbeul", "L’Ancien Jeune", "Le Joueur de Flûte du Hall C", "Le Nébuleux", "Tonton Yop",
    "Frérot Sans Histoire", "Tajine Sauvage", "Vlad le SDF", "El Survêt", "Wallah Boy", "Jamel de Vitry", "Brigadier Tarpin",
    "Le Cousin qui Dort Jamais", "Zekri la Galère", "Monsieur Barrette", "Rayan Sniffe", "Chawarma Spirit", "Kebabos", "La Légende du Palier",
    "Tchoupi le Rôdeur", "Kalash Sans Chargeur", "Le Gars d’en Face", "Boutch le Flou", "Foufou du Banc", "Le Mec au Fond du Snap",
    "Le Fils à Personne", "Rebeu Ancestral", "Chef Sans Forfait", "Momo du Dernier", "Tonton Placard", "La Fringale",
    "Le Zarma King", "Choufman", "Mika la Rumeur", "El Biloute", "El Bagarre", "L'Inspecteur Barrette", "L’Éclair du 93",
    "Captain Injustifié", "Sultan Binks", "Hakim Zarma", "Karim la Panique", "Abdel Fatal", "Le Chomeur Suprême"
]

CLANS = [
    "Famille du Ghetto",
    "Clan du Croissant",
    "Dynastie des Potos",
    "Secte du Grillav",
    "Team du Kebab",
    "Crew du Zebi",
    "Brigade du Quartier",
    "Ligue des Babtous",
    "Famille Siffredi",
    "La Street Family",

    # ADDITIONS ENORMES
    "Ordre des Survets Sacrés",
    "Tribu des Yeux Rouges",
    "Secte des Sans-Caf",
    "Famille du HLM Maudit",
    "Dynastie du Banc Cassé",
    "Clan du Dernier Joint",
    "Compagnie des Daronnes Furieuses",
    "Cercle des Mangeurs de Semoule",
    "Confrérie du Hall 7",
    "Légion des Non-Rappelés",
    "Fraternité de la Barrette Sacrée",
    "Union des Parkings Obscurs",
    "Cartel des Grecs Maudits",
    "Guilde des Boostés à la Bourse",
    "Empire des Fauteuils Volés",
    "Clan du Couscous Royal",
    "Commando du 93 Profond",
    "Famille des Burnés d’Ikea",
    "Ordre Mystique des Chargeurs Cassés",
    "Famille TikTokaïne",
    "Réseau des Pères Inconnus",
    "Dynastie des Mecs du Banc",
    "Compagnie du Dernier Snap",
    "Secte des Voyants Sans Forfait",
    "Famille des Michto Survivants",
    "Crew des Faux Malades CAF",
    "Association des Démons Sans Permis",
    "Confrérie de la Plaquette Oubliée",
    "Dynastie des Prénoms à problème",
    "Union Sacrée des Darons Oubliés",
    "Commune Libre de la Barrette Perdue",
    "Cartel des Silences Louches",
    "Clan des Semelles Usées",
    "Armée des Tontons Chelous",
    "République Indépendante du Palier B",
    "Fraternité des Grillav Oubliés",
    "Coalition des Balcons en Chicha",
    "Cercle Secret des Djeunz Égarés",
    "Congrégation des Paranoïas Partagées"
]

CITATIONS = [
    "Avec un blaze pareil, tu croques la vie à pleine dents, wallah.",
    "On te cherche, mais personne t’égale, frère.",
    "T’as la street dans l’ADN, c’est validé.",
    "Les jaloux vont maigrir, la famille.",
    "Ta daronne pleure de fierté chaque matin.",
    "Le destin, c’est toi qui l’inventes.",
    "Zarma tu régales la ville avec ce prénom.",
    "Avec un blaze comme ça, même les condés veulent un selfie.",
    "Ton prénom résonne jusqu’au bled.",
    "T’es la légende du Hall 7, wallah.",

    # ADDITIONS ÉNORMES
    "T’as un blaze qu’on grave sur les murs et dans les cœurs.",
    "Même les voyants te voient arriver dans leurs visions.",
    "T’es pas une légende urbaine, t’es une prophétie de quartier.",
    "Quand tu marches, le sol t’écoute, zebi.",
    "Ton prénom c’est un freestyle, chaque syllabe kicke.",
    "T’as été sculpté par les astres et les bastos.",
    "Le silence se tait quand t’arrives, wallah.",
    "T’es pas né sous une étoile, t’es l’étoile qu’on attendait.",
    "Ton blaze, c’est du ciment pour les âmes fracturées.",
    "T’as mis la street en PLS avec juste ton regard.",
    "T’as pas choisi ton prénom, c’est lui qui t’a choisi, habibi.",
    "Même les manouches prient pour avoir ta prestance.",
    "Ton prénom s’écrit en majuscules, même sur les tags.",
    "La rue te cite sans te comprendre – t’es au-dessus.",
    "T’as grandi dans l’ombre pour mieux briller en plein jour.",
    "T’es le genre de mec qu’on respecte même en rêve.",
    "Ton prénom a le goût du charbon, de la sueur et de la gloire.",
    "T’as traversé les galères comme Moïse la mer, sans une goutte sur le survêt.",
    "T’es la réponse aux prières de ton quartier.",
    "Ton prénom fait trembler les claviers d’la CAF.",
    "T’as l’élégance d’un gitan en costume trois pièces.",
    "T’as pas percé, t’as transpercé le game.",
    "T’es la démo vivante qu’on peut être loyal sans être con.",
    "Ton blaze, c’est du feu d’artifice sur fond de darwa."
]

HOROSCOPE = [
    "Aujourd'hui tu vas esquiver les condés, inchallah.",
    "Prépare-toi, la chance arrive, mais pas pour tout le monde.",
    "Un kebab t’attend ce midi, la street te sourit.",
    "Reste à l’affût, un coup de trafalgar arrive.",
    "Le respect s’obtient, tu le sais déjà.",
    "La BAC est dans le secteur, baisse le son.",
    "Les astres valident ta dégaine, fais-toi plaisir.",
    "T’as la vibe, profite, mais oublie pas la mif.",
    "Quelqu’un va t’appeler, ça va changer ta journée.",
    "C’est ton jour de gloire… ou de galère, choisis bien.",

    # ADDITIONNEL
    "Mars est en clash avec Mercure, évite les embrouilles à la chicha.",
    "T'as un face-à-face avec ton destin dans l’ascenseur du bâtiment C.",
    "Ne réponds pas aux appels inconnus, c’est pas ton jour pour te faire cramer.",
    "Ton ex va stalk ton profil aujourd’hui, sois frais(e).",
    "T’as un coup de génie qui t’arrive en plein shit, prends note wallah.",
    "Ton chargeur va te lâcher, mais ton mental non.",
    "Le ciel t’envoie une lumière : un grec gratuit ou un plan foireux ? À toi de voir.",
    "Balance pas trop d’stories aujourd’hui, t’attires le mauvais œil.",
    "Ton pote va t’trahir pour une canette. Pardonne, mais oublie jamais.",
    "T’as un karma de boucher aujourd’hui, mais utilise-le bien.",
    "La prochaine personne qui te regarde chelou, c’est elle ton test cosmique.",
    "Saturne te conseille de pas faire le fou en caisse volée.",
    "T’as un charisme cosmique, les murs murmurent ton prénom.",
    "Évite les balances aujourd’hui, Pluton les rend plus actives que d’hab.",
    "Tu vas recroiser un ancien. S’il te tend la main, regarde s’il cache un couteau.",
    "T’es à deux doigts de percer… ou de percer un pneu, fais le bon choix.",
    "Ton signe astral c’est le chacal, agis en chef de meute.",
    "Si tu sors avec tes Nike, la réussite colle à tes semelles.",
    "Tes chakras sont alignés mais ta carte SIM bug, reste focus.",
    "T’as la prestance d’un lion mais les dettes d’un pigeon – équilibre, frère.",
    "Une meuf chelou va te snapper. Réfléchis avant d’envoyer une voix.",
    "Ce soir t’as un rêve bizarre. C’est pas juste un rêve, c’est un message du bendo astral.",
    "Méfie-toi de l’eau plate aujourd’hui. Tout ce qui est calme, cache un traquenard.",
    "Les étoiles te murmurent : évite les placements cryptos chelous aujourd’hui.",
    "Ton blaze va sortir de la bouche d’un ancien – t’es dans les légendes ou les dossiers ?"
]

CRED_BADGES = [
    (100, "👑 Dieu du bendo – Même les anciens t’écoutent sans parler."),
    (98, "🦾 Crédibilité atomique – Ton blaze fait trembler la dalle."),
    (96, "🔮 Légende vivante – Ton nom circule en chuchotement."),
    (94, "⚔️ Validé même à Fleury – Zarma t’as des dossiers."),
    (92, "🐐 Le goat du quartier – On murmure ton blaze à la mosquée."),
    (90, "🦾 Crédibilité absolue – La street te salue !"),
    (88, "💎 Trop précieux – Même les gitans veulent t’adopter."),
    (86, "🎭 Tu bluffes personne mais t’es respecté."),
    (84, "🧠 Stratégique – T’es pas violent mais t’es dangereux."),
    (82, "🛸 Tu planes au-dessus des embrouilles."),
    (80, "🦍 Alpha tranquille – T’as pas besoin de crier pour dominer."),
    (78, "🎯 Toujours là quand faut agir – sniper de la street."),
    (76, "🎖️ Officiel de la zone – t’as ton badge dans les halls."),
    (74, "💯 Validé par tous les quartiers !"),
    (72, "🤝 Bien vu – même les daronnes te respectent."),
    (70, "🔧 Tu répares la street avec tes conseils."),
    (68, "🐕 Loyal, utile, discret – genre pitbull en costard."),
    (66, "🎒 Ancien en reconversion – plus sage que hardcore."),
    (64, "🛹 Tu traînes, mais tu parles pas trop."),
    (62, "📦 Livre les bails, sans faire le mec."),
    (60, "🔥 Respecté dans la plupart des halls."),
    (58, "🚬 Présent mais discret – t’as pas le blaze qui marque."),
    (56, "📵 On t’appelle jamais mais t’es pas un rat."),
    (54, "🪑 T’es assis dans la zone mais personne t’écoute."),
    (52, "🧊 Trop froid pour exister, trop tiède pour choquer."),
    (50, "💺 Passager dans le bus de la street."),
    (48, "🪞 T’es là pour refléter les autres."),
    (46, "🪙 T’as une pièce, mais pas de valeur."),
    (44, "📉 Chaque embrouille te fait baisser de level."),
    (42, "🌫️ Inoffensif mais chelou – genre brouillard chelou."),
    (40, "🫣 Moyen, évite d’aller à La Courneuve seul."),
    (38, "🎐 Tu flottes, mais personne te capte."),
    (36, "🚪 T’es la porte qu’on claque sans prévenir."),
    (34, "🪰 Tu déranges plus qu’autre chose."),
    (32, "🥽 Même en te regardant on te voit pas."),
    (30, "🦴 T’es le snack du quartier."),
    (28, "🐌 Trop lent pour le game."),
    (26, "🧻 Jetable – t’es utile une fois."),
    (24, "🫥 Ton blaze s’évapore dans les halls."),
    (22, "🧺 On t’a oublié au lavomatique."),
    (20, "💤 Crédibilité en PLS, t’es invisible."),
    (18, "🥴 Même les pigeons t’ignorent."),
    (16, "👣 T’es les traces de pas de quelqu’un d’autre."),
    (14, "🪦 La street t’a enterré vivant."),
    (12, "🐀 Même les balances veulent pas de toi."),
    (10, "🚽 Tu sers qu’à tirer la chasse."),
    (8,  "🪳 T’es une blatte sans destination."),
    (6,  "🥫 T’as été mis en conserve pour rien."),
    (4,  "🧟 Zombie de quartier – personne te réveille."),
    (2,  "🫗 Vide comme un snap sans vue."),
    (0,  "🥔 Zarma tu fais pitié frère, personne te calcule.")
]

INSULTES = [
    "T’es une chips wallah !",
    "Même ta daronne voulait un autre blaze.",
    "Avec ce prénom tu fais même pas peur aux pigeons.",
    "Wallah c’est éclaté au sol ton blaze.",
    "La honte à la famille, zebi.",
    "La street t’a oublié avant même de te connaître.",
    "T’es en soldes toute l’année avec ce blaze.",
    "Même les robots ont plus de style.",
    "T’es plus rare qu’un kebab végane.",

    # NOUVELLES INSULTES
    "Ton prénom sonne comme une appli Android pas finie.",
    "T’as été nommé par un bug d’IA wallah.",
    "Même les Télétubbies t’auraient recalé.",
    "Ton blaze ? C’est un patch note foireux.",
    "T’as le prénom d’un pigeon en PLS.",
    "Ton blaze, c’est du AirFryer sans air ni fryer.",
    "T’es la version wish d’un blaze stylé.",
    "T’as été codé en HTML sans CSS.",
    "Même un captcha te laisserait passer sans te tester.",
    "T’as un prénom à te faire recaler d’un camp gitan.",
    "T’es un 404 de la dignité, zebi.",
    "T’as le flow d’un PowerPoint de 6e.",
    "Ton blaze fait rire les élèves d’ULIS.",
    "Même les bots de scam veulent pas de toi.",
    "T’as un blaze de tiktokeur refoulé par la CNIL.",
    "Même les témoins de Jéhovah zappent ta sonnette.",
    "Ton prénom c’est un ban direct sur Discord.",
    "T’as un blaze qui sent la vanne périmée.",
    "Avec ce prénom, t’es même pas invité aux barbecues.",
    "Ton prénom c’est du spam émotionnel.",
    "T’as été généré par ChatGPT version bourrée.",
    "Ton blaze fait saigner les oreilles de l’alphabet.",
    "T’as le charisme d’un ticket de caisse froissé.",
    "Même les schmitts veulent pas te contrôler.",
    "Ton prénom, c’est l’écran bleu de la vie.",
    "On dirait que t’as été nommé par un stagiaire sourd.",
    "Ton blaze a été généré par un bébé manouche sous skunk.",
    "Même les gitans t’appellent 'frérot' sans te calculer.",
    "Ton blaze ? C’est une faute d’orthographe validée.",
    "T’es le seul à porter ce prénom, et c’est pas un compliment.",
    "Ton blaze rime avec PLS."
]

PRENOMS_GITANS = [
    "Zlatko", "Donovan", "Nikita", "Mickaëlo", "Django", "Manouchka", "Angelo", "Tzigane",
    "Mirko", "Rodrigo", "Ludivina", "Petra", "Mélinda", "Raymondo", "Maria-La-Loco",

    # Prénoms hommes
    "Santino", "Zoran", "Yanko", "Milovan", "Ionel", "Stefan", "Alonzo", "Vano", "Ruben",
    "Isandro", "Petru", "Cosmin", "Jasko", "Jovan", "Nicolae", "Aleko", "Sacha", "Ionut",
    "Tchico", "Mariano", "Zorba", "Alexandro", "Sulejman", "Lubo", "Yuri", "Damiano",

    # Prénoms femmes
    "Esmeralda", "Nadja", "Ludmila", "Svetlana", "Sabrina", "Gordana", "Tatiana", "Yelena",
    "Zina", "Tania", "Anastazia", "Sofika", "Marushka", "Flamenca", "Sorina", "Calista",
    "Katarina", "Velma", "Ramona", "Mirella", "Zorana", "Giuliana", "Chayana", "Shéhérazade",

    # Blazes mixtes et stylés
    "Louna-Rose", "Angélo-Djo", "Zéfir", "Djo", "Zinga", "Tanya-Luna", "Manolo", "Mikaï", "Tano", "Joska"
]


def lire_blaze_hits():
    if os.path.exists(BLAZE_HITS_PATH):
        with open(BLAZE_HITS_PATH, 'r') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def incr_blaze_hits(blaze):
    hits = lire_blaze_hits()
    hits[blaze] = hits.get(blaze, 0) + 1
    with open(BLAZE_HITS_PATH, 'w') as f:
        json.dump(hits, f)
    return hits[blaze]

def leaderboard():
    hits = lire_blaze_hits()
    sorted_hits = sorted(hits.items(), key=lambda x: x[1], reverse=True)
    return [{"prenom": p, "tests": n} for p, n in sorted_hits[:10]]

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
    n_tests = incr_blaze_hits(prenom)
    surnom = random.choice(SURNOMS_STREET)
    clan = random.choice(CLANS)
    citation = random.choice(CITATIONS)
    respect = min(100, max(3, int(100 - abs(prix - 100) + random.uniform(-8, 8))))
    cred_txt = next(txt for seuil, txt in CRED_BADGES if respect >= seuil)
    original = 100 - int((freq / FREQ_MAX) * 100) if freq else 100
    horoscope = random.choice(HOROSCOPE)
    insulte = random.choice(INSULTES)
    return jsonify({
        "prix": prix,
        "popularite": freq,
        "lettres": n_lettres,
        "voyelles": n_voyelles,
        "consonnes": n_consonnes,
        "lettres_rares": n_rares,
        "bonus_tiret": is_tiret,
        "genre": genre_code,
        "surnom": surnom,
        "clan": clan,
        "citation": citation,
        "respect": respect,
        "cred_txt": cred_txt,
        "original": original,
        "n_tests": n_tests,
        "horoscope": horoscope,
        "insulte": insulte
    })

@app.route('/api/leaderboard')
def api_leaderboard():
    return jsonify(leaderboard())

@app.route('/api/quiz')
def api_quiz():
    valid_prenoms = [p for p in prenoms.keys() if prenoms[p] > 0]
    quiz_prenom = random.choice(valid_prenoms)
    freq = prenoms.get(quiz_prenom, 0)
    n_lettres = len(quiz_prenom)
    n_voyelles, n_consonnes = compter_voyelles_consonnes(quiz_prenom)
    n_rares = compter_lettres_rares(quiz_prenom)
    is_tiret = '-' in quiz_prenom or "'" in quiz_prenom
    if freq == 0:
        prix = 200
    else:
        logfreq = math.log(freq + 1)
        logmax = math.log(FREQ_MAX + 1)
        base = 200 * (1 - (logfreq / logmax))
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
    prix = min(200, max(10, round(prix, 2)))
    return jsonify({"prenom": quiz_prenom.capitalize(), "prix": prix})

@app.route('/api/zigzig')
def zigzig():
    prenom = request.args.get("prenom", "").strip().lower()
    genre = request.args.get("genre", "M")  # "M", "F", "X"
    n_lettres = len(prenom)
    n_voyelles, n_consonnes = compter_voyelles_consonnes(prenom)
    n_rares = compter_lettres_rares(prenom)
    score = 5
    score += max(0, n_lettres - 4) * 1.5
    score += n_voyelles * 0.8
    score += n_consonnes * 1.1
    score += n_rares * 3.5
    if "-" in prenom or "'" in prenom:
        score += 1.5
    score += random.uniform(-2, 2)
    score = int(max(0, min(20, round(score))))
    if genre == "F":
        phrases = [
            "Tu zigzig même pas les regards !",
            "Aucune daronne n’est jalouse de toi.",
            "Bof, niveau zigzig t’es sage.",
            "T’as pas fait vibrer beaucoup de mecs.",
            "Ton nom fait plus fuir que fantasmer.",
            "Zarma la voisine te regarde même pas.",
            "T’as un crush, mais il t’a ghosté.",
            "Sympa mais discrète, on te voit pas !",
            "Mi-fleur bleue, mi-chiante.",
            "Commence à sortir plus pour voir du monde !",
            "Zigzig léger, ça s'échauffe.",
            "Pas mal, la street valide tes vibes.",
            "Bientôt la queen des DM !",
            "Tu fais tourner des têtes, wallah.",
            "La légende locale du zigzig.",
            "Ça matche sur Tinder, fais gaffe.",
            "La rivale des influenceuses.",
            "Méfie-toi, les jalouses t’espionnent.",
            "Wallah tu traumatise les gars du quartier.",
            "C’est bon, t’as cassé tous les cœurs, zebi !"
        ]
        avatars = ["notionists", "adventurer-neutral", "micah", "miniavs", "fun-emoji", "personas", "pixel-art", "rings", "shapes", "bottts"]
    else:
        phrases = [
            "Aucune meuf veut te zigzig, wallah !",
            "Même Tinder te met sur écoute.",
            "Zigzig inexistant, c’est la dèche.",
            "Les keufs te calculent plus que les meufs.",
            "Ton blaze fait fuir les zouz.",
            "Zarma t’es pote avec tout le monde, mais rien de plus.",
            "T’as tenté, mais la friendzone t’a ken.",
            "On t’appelle Casimir, pas Casanova.",
            "Moyen, la mif croit encore en toi.",
            "T’as brillé au mariage de ta cousine, c’est tout.",
            "Zigzig discret, mais prometteur.",
            "La street commence à parler de toi.",
            "Tu peux finir en légende, inchallah.",
            "T’es validé à Grigny.",
            "Les zouz aiment bien ton style.",
            "T’es l’espoir du quartier.",
            "On te respecte au barbecue.",
            "Wallah, tu peux tout casser cet été.",
            "La daronne commence à s’inquiéter.",
            "Rocco, tu fais plaisir à toutes les femmes !"
        ]
        avatars = ["bottts", "rings", "adventurer", "pixel-art", "personas", "notionists", "miniavs", "adventurer-neutral", "micah", "shapes"]
    phrase = phrases[min(score, len(phrases)-1)]
    avatar = avatars[score % len(avatars)]
    url = f"https://api.dicebear.com/7.x/{avatar}/svg?seed=zigzig{score}{prenom}"
    return jsonify({
        "score": score,
        "phrase": phrase,
        "avatar": url
    })

@app.route('/api/compatibilite')
def api_compatibilite():
    prenom1 = request.args.get("prenom1", "").strip().lower()
    prenom2 = request.args.get("prenom2", "").strip().lower()
    if not prenom1 or not prenom2:
        return jsonify({"ok": False, "msg": "Donne deux blazes !"})
    base = sum(ord(x) for x in prenom1 + prenom2)
    compat = ((base % 97) + random.randint(0, 20)) % 101
    msg = f"Compatibilité : {compat} % – "
    if compat > 90:
        msg += "Parfait, vous allez faire 12 gosses à Grigny !"
    elif compat > 70:
        msg += "Solide, ça va buzzer sur Snap !"
    elif compat > 50:
        msg += "Pas mal, la street valide ce duo."
    elif compat > 30:
        msg += "Mouais, y'a un bail chelou."
    else:
        msg += "Laisse tomber, y'aura pas de zigzig."
    return jsonify({"ok": True, "score": compat, "msg": msg})

@app.route('/api/gitan')
def api_gitan():
    prenom = random.choice(PRENOMS_GITANS)
    return jsonify({"prenom": prenom})

@app.route('/api/insulte')
def api_insulte():
    prenom = request.args.get("prenom", "").strip().lower()
    return jsonify({"insulte": random.choice(INSULTES)})

@app.route('/api/son')
def api_son():
    # MOCK : à brancher avec une API de synthèse vocale si tu veux (moteur IA style PlayHT, ElevenLabs, etc.)
    return jsonify({"url": "https://www.myinstants.com/media/sounds/ratpi-world.mp3"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
