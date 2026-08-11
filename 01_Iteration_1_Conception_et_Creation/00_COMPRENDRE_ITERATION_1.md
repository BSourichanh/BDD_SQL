# 🎓 Guide de Compréhension — Itération 1 : Conception & Création de la BDD

Ce document résume **tout ce qu'il faut comprendre et maîtriser** pour l'Itération 1 (Conception et modélisation relationnelle).

---

## 📍 Étape 1 : Analyse du Cahier des Charges & Use Cases
- **Ce qu'il faut comprendre** : Avant de coder, il faut identifier les entités métier (ex: Particuliers, Transporteurs, Clients, Colis, Missions).
- **Les Use Cases (Cas d'utilisation)** : Modéliser le cycle de vie des données (*ex: Réception d'un colis -> Stockage en Point Relais -> Retrait Client ou Retour Transporteur*).

---

## 📍 Étape 2 : Conventions de Nommage
- **Ce qu'il faut comprendre** : Une base propre suit des règles strictes.
  - **Tables** : `snake_case` au pluriel (`points_relais`, `transporteurs`, `colis`).
  - **Colonnes** : `snake_case` au singulier (`code_postal`, `date_livraison`).
  - **Clés primaires (PK)** : `id_<table_singulier>` (`id_colis`, `id_point_relais`).
  - **Clés étrangères (FK)** : `id_<table_cible_singulier>` (`id_transporteur`).

---

## 📍 Étape 3 : Le Dictionnaire de Données
- **Ce qu'il faut comprendre** : C'est le tableau de référence répertoriant chaque champ de la BDD avec son type, sa taille et ses contraintes (`NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`).

---

## 📍 Étape 4 : Le MCD (Modèle Conceptuel de Données - Merise)
- **Ce qu'il faut comprendre** :
  - **Entités** (Rectangles) : Représentent les objets du monde réel.
  - **Associations** (Ellipses) : Représentent les liens entre entités.
  - **Cardinalités** :
    - `0,1` / `1,1` : Au plus un / un et un seul.
    - `0,N` / `1,N` : Zéro à plusieurs / au moins un à plusieurs.

---

## 📍 Étape 5 : Le MLD (Modèle Logique de Données)
- **Ce qu'il faut comprendre** : Transformation du MCD en tables relationnelles.
  - Relation `(1,1)` à `(0,N)` : La clé primaire du côté `N` devient **Clé Étrangère (FK)** dans l'autre table.
  - Relation `(0,N)` à `(0,N)` : Création d'une **Table d'Association** spécifique contenant les clés primaires des 2 tables.

---

## 📍 Étape 6 : Scripts SQL DDL & DML
- **DDL (Data Definition Language)** : `CREATE TABLE` avec types (`INT`, `VARCHAR`, `DATETIME`, `ENUM`), `PRIMARY KEY` et `FOREIGN KEY ... REFERENCES`.
- **DML (Data Manipulation Language)** : `INSERT INTO` pour alimenter les tables de test.
