# Valeur de ton prénom (INSEE Edition)

**Projet street pour estimer la "valeur" de n'importe quel prénom français entre 0 et 200€, selon sa rareté officielle, avec les vraies stats INSEE (de 1900 à 2022).**

## ⚡️ Installation & lancement

1. Clone ou télécharge ce dossier.
2. Télécharge le vrai CSV INSEE ici (c'est lourd, +150Mo dézippé) :  
   [Télécharger prenoms.csv.zip (lien direct)](https://www.data.gouv.fr/fr/datasets/r/24f1f4aa-87a0-4b16-88b6-8591e62a08bc)
3. Dézippe et mets le fichier `prenom.csv` à la racine du projet (à côté de app.py).
4. Installe les dépendances :
    ```
    pip install -r requirements.txt
    ```
5. Lance le serveur :
    ```
    python app.py
    ```
6. Va sur [http://localhost:5000](http://localhost:5000) et amuse-toi.

## 🔥 Déploiement Railway/GitHub

- Tout est prêt à être push sur GitHub et connecté à Railway.
- Mets bien `prenom.csv` dans le repo, et ajoute si besoin un fichier `Procfile` :
    ```
    web: python app.py
    ```
- C'est plug & play, tu n'as rien d'autre à faire.

## ⚠️ Attention

- Si `prenom.csv` n'est pas trouvé, rien ne marche !
- Le script utilise toutes années confondues pour la popularité.

## 👊 Par la street, pour la street.

