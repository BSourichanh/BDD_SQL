# 📚 Guide Complet & Explicatif des Étapes du Projet BDD SQL (Format Moodle)

> [!INFO] **Informations du Cours Moodle**
> **Formation** : BDD SQL DEVAA2028 — Jour 2&3 : Projet SQL - Conception et Création
> **Plateforme** : Go2Moodle (Ingenium Digital Learning)
> **Objectif Général** : Concevoir, implémenter et sécuriser une base de données relationnelle répondant au cahier des charges de la plateforme de livraison de colis en points relais.

---

## 📑 Sommaire des Étapes & Liens Moodle

- [ITÉRATION 1 : CONCEPTION](#it%C3%A9ration-1--conception)
  - [1.1 | Cahier des charges](#11--cahier-des-charges-1h--bin%C3%B4me)
  - [1.2 | Préparation & Conventions](#12--pr%C3%A9paration-05h--bin%C3%B4me)
  - [1.3 | Dictionnaire des données](#13--dictionnaire-1h--bin%C3%B4me)
  - [1.4 | Modèle Conceptuel de Données (MCD)](#14--mod%C3%A8le-conceptuel-de-donn%C3%A9es-mcd-75h--bin%C3%B4me)
  - [1.5 | Modèle Logique de Données (MLD)](#15--mod%C3%A8le-logique-de-donn%C3%A9es-mld-1h--bin%C3%B4me)
  - [1.6 | Script création base de données & Remplissage](#16--script-cr%C3%A9ation-base-de-donn%C3%A9es-3h--bin%C3%B4me)
- [ITÉRATION 2 : SÉCURISATION](#it%C3%A9ration-2--s%C3%A9curisation)
  - [2.1 | Vulnérabilités SQL](#21--vuln%C3%A9rabilit%C3%A9s-sql-bin%C3%B4me)
  - [2.2 | Mise en place des correctifs](#22--mise-en-place-bin%C3%B4me)
- [📦 Synthèse des Livrables Moodle](#-synth%C3%A8se-des-livrables-moodle)

---

# ITÉRATION 1 : CONCEPTION

## 1.1 | Cahier des charges (~1h | ⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Concevoir une base de données à partir d'un cahier des charges réel.

### 📜 Contexte Métier (Extraits du Cahier des Charges)
Une entreprise souhaite mettre en place une plateforme permettant à des particuliers de proposer leur domicile comme **point relais** pour la livraison de colis, en collaboration avec des **transporteurs partenaires** et à destination de **clients finaux destinataires**.

1. **Particuliers (Points Relais)** : Inscription via un compte personnel (identité, adresse, contact, logement, disponibilités). Leur activation dépend de leur éligibilité vis-à-vis des besoins des transporteurs.
2. **Missions** : Lorsqu'un particulier est accepté par un transporteur, une mission de point relais est mise en place pour une période donnée.
3. **Colis & Cycle de Livraison** :
   - Pris en charge par le transporteur.
   - En cours de livraison $\rightarrow$ Remis au point relais si livraison à domicile impossible.
   - Conservé temporairement au point relais $\rightarrow$ Remis au client final.
   - **Règle des 14 jours** : Si le client ne récupère pas son colis sous 14 jours, le colis devient **non réclamé** et passe en processus de retour.
   - **Retour** : Reste temporairement au point relais jusqu'à récupération par le transporteur $\rightarrow$ Processus terminé.
4. **Traçabilité & Historique** : Conserver l'historique complet des changements d'état (dates, point relais, transporteur).
5. **Administration** : Interface d'administration pour suivre les colis, retraits en attente, retours et missions.

### 👣 Déroulement Pas à Pas
1. **Échange en binôme** : Discuter de la compréhension du cahier des charges et identifier toutes les données indispensables.
2. **Analyse par Scénarios (*Use Cases*)** : Lister ce qu'un client, un point relais ou un administrateur devra réaliser.
3. **Centralisation** : Rédiger et centraliser ces éléments dans votre **Dossier de Conception**.

> [!TIP] **Astuce Moodle**
> Le formateur joue le rôle du représentant du client. Posez-lui des questions pour préciser les zones d'ombre ou valider vos choix !

---

## 1.2 | Préparation (~0.5h | ⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Fixer les règles de fonctionnement et les conventions de nommage à suivre tout au long du projet.

### 👣 Déroulement Pas à Pas
1. **Échange sur les pratiques** : S'accorder au sein du binôme sur les normes de nommage (tables, champs, notations, types de variables).
2. **Rédaction des conventions** : Compléter le dossier de conception en y consignant ces règles :
   - Noms des tables en `snake_case` au **pluriel** (ex: `particuliers`, `colis`).
   - Noms des champs au **singulier** (ex: `code_postal`, `date_livraison`).
   - Clés Primaires (`id_<table_singulier>`) et Clés Étrangères (`id_<table_cible_singulier>`).
3. **Prise en main des outils Merise** : Se renseigner sur la méthode Merise et installer un outil de modélisation (ex: AnalyseSI).

### 🔗 Ressources Officiellement Recommandées par Moodle
- 📖 [Initiation à la méthode Merise (Developpez.com)](https://ineumann.developpez.com/tutoriels/merise/initiation-merise/)
- 📖 [Guide des Bases de Données - Méthode Merise](https://www.base-de-donnees.com/merise/)
- 📖 [Cours complet Conception BDD Relationnelle (Cours-Gratuit)](https://www.cours-gratuit.com/cours-merise/cours-merise-conception-d-une-base-de-donnees-relationnelle)
- 🌐 [Article Wikipedia — Merise (Informatique)](https://fr.wikipedia.org/wiki/Merise_(informatique))
- 🛠️ [Téléchargement d'AnalyseSI (Launchpad)](https://launchpad.net/analysesi)

---

## 1.3 | Dictionnaire (~1h | ⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Créer le dictionnaire de données complet en énumérant toutes les données à sauvegarder.

### 👣 Déroulement Pas à Pas
1. Créer le dictionnaire dans l'outil de votre choix avec au minimum les 4 colonnes requises par Moodle :
   - **Code Mnémonique** (Nom de la colonne SQL)
   - **Désignation** (Libellé explicatif en français)
   - **Type** (`VARCHAR`, `INT`, `DECIMAL`, `DATETIME`, `BOOLEAN`, `ENUM`)
   - **Taille & Contraintes** (`NOT NULL`, `UNIQUE`, `CHECK`)
2. Remplir le dictionnaire de manière la plus **exhaustive** possible.
3. Ajouter le dictionnaire au **Dossier de Conception**.

---

## 1.4 | Modèle conceptuel de données (MCD) (~7.5h | ⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Structurer les données du dictionnaire sous forme d'un **Modèle Entité-Association (MCD)**.

### 👣 Déroulement Pas à Pas
1. **Création des Entités** :
   - Rectangle avec le nom de l'entité en en-tête.
   - Attribut unique (identifiant / clé primaire) placé en première position.
   - Exemples d'entités : `PARTICULIER`, `TRANSPORTEUR`, `CLIENT`, `COLIS`.
2. **Création des Associations & Cardinalités** :
   - Relier les entités par des associations nommées par des verbes.
   - Poser les cardinalités selon le formalisme Merise :
     - `0-1` : Lié à une ou aucune entité.
     - `1-1` : Lié à une et une seule entité.
     - `0-n` : Lié à aucune ou au moins une entité.
     - `1-n` : Lié à au moins une entité.
     - `n-n` : Plusieurs entités liées à plusieurs entités (ex: missions).

> [!WARNING] **Astuce Moodle**
> `/!\ Attention à la position des cardinalités ! /!\`
> Vérifiez bien le sens de chaque association (ex: un colis est chez au plus 1 point relais à un instant donné `0-1`, alors qu'un point relais peut garder `0-n` colis).

---

## 1.5 | Modèle logique de données (MLD) (~1h | ⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Transformer le MCD en schéma relationnel de tables SQL selon les 3 règles de passage Merise.

### 👣 Déroulement Pas à Pas (3 Cas de figure Moodle)
1. **Relation `0-1 (ou 1-1)` & `0-1 (ou 1-1)`** :
   - Les deux entités sont liées entre elles.
   - La clé primaire de chaque entité est ajoutée comme clé étrangère dans l'autre (ou fusion).
2. **Relation `0-1 (ou 1-1)` & `0-n (ou 1-n)`** :
   - La clé primaire de l'entité du côté `N` est ajoutée comme **Clé Étrangère (FK)** dans la table du côté `1`.
3. **Relation `0-n (ou 1-n)` & `0-n (ou 1-n)`** :
   - Création d'une **Table d'Association** intermédiaire.
   - Les clés primaires des deux entités sont ajoutées à cette table sous forme de clés étrangères composites.
4. Remplacer les relations par des flèches allant des clés étrangères vers les clés primaires correspondantes.
5. Intégrer le schéma MLD au **Dossier de Conception**.

---

## 1.6 | Script création base de données (~3h | ⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Rédiger les scripts SQL de création de la base de données (DDL) et de remplissage (DML).

### 👣 Déroulement Pas à Pas

#### 1. Classification par Niveau de Dépendance
Classer les tables selon leur niveau de dépendance pour déterminer l'ordre de création :
- **Niveau 0** : Aucune clé étrangère (`transporteurs`, `clients`, `particuliers`).
- **Niveau 1** : Lié à au moins une table de Niveau 0 (`missions`).
- **Niveau 2** : Lié à au moins une table de Niveau 1 (`colis`).
- **Niveau 3** : Traçabilité (`historique_statuts_colis`).

#### 2. Script de Création DDL (`schema.sql`)
- Création de la BDD : `CREATE DATABASE bdd_colis_relais;`
- Création des tables : `CREATE TABLE ...` avec Clés Primaires (simples ou multiples), Clés Étrangères (`FOREIGN KEY ... REFERENCES`), types et contraintes `CHECK`.

#### 3. Test & Comparaison du Schéma
- Exécuter le script sur votre serveur SQL (MySQL / MariaDB).
- Générer le schéma de la BDD créée et le comparer avec le MLD théorique.

#### 4. Script de Remplissage DML (`seeds.sql`)
- Insérer les données de base (liste des transporteurs et statuts).
- Insérer les données de fonctionnement couvrant tous les Use Cases (un colis tout juste créé, un colis arrivé en relais, un colis retiré, un colis non réclamé après 14 jours, un colis en retour).

### 🔗 Liens de Cours SQL Recommandés par Moodle
- 🌐 [Cours SQL.sh — CREATE DATABASE](https://sql.sh/cours/create-database)
- 🌐 [Cours SQL.sh — CREATE TABLE](https://sql.sh/cours/create-table)
- 🌐 [Cours SQL.sh — INSERT INTO](https://sql.sh/cours/insert-into)

---

# ITÉRATION 2 : SÉCURISATION (Optionnel / Avancé)

## 2.1 | Vulnérabilités SQL (⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Rechercher les vulnérabilités liées aux bases de données SQL, notamment lors d'un accès depuis un programme Java/PHP, du stockage des données sensibles ou des paramètres d'accès.

### 👣 Déroulement Pas à Pas
1. Rechercher les risques principaux :
   - **Injections SQL** (concaténation directe de requêtes).
   - Mots de passe stockés en texte brut.
   - Identifiants BDD codés en dur (*hardcoded credentials*).
2. Rédiger un **Mémo de Sécurité** centralisant les pratiques de protection.
3. Tester la réactivité du programme applicatif.

---

## 2.2 | Mise en place (⚙ Autonomie | 👥 Travail en binôme)

### 🎯 Objectif Moodle
Corriger et sécuriser l'application Java/PHP et le serveur BDD.

### 👣 Déroulement Pas à Pas
1. Mettre à jour les classes et méthodes vulnérables en utilisant des requêtes préparées (`PreparedStatement`).
2. Tenter de reproduire les injections SQL pour vérifier la résistance du code.
3. Appliquer un patch sur la base de données si nécessaire.
4. Réviser le stockage des paramètres de connexion (utilisation d'un fichier `.env` non versionné).

---

## 📦 Synthèse des Livrables Moodle

### 📥 Livrables de l'Itération 1
- [x] **Dossier de Conception** complet (Conventions, Dictionnaire de données, MCD, MLD).
- [x] **Le schéma de la base de données** généré.
- [x] **Le script SQL de création DDL** (`04_schema_creation.sql`).
- [x] **Le script SQL d'insertion DML** (`05_insertion_donnees.sql`).

### 📥 Livrables de l'Itération 2
- [x] **Le Mémo des failles de sécurité SQL** (`06_memo_securite_sql.md`).
- [x] **La base de données mise à jour / patchée**.
- [x] **Le code d'accès aux données protégé** (`PreparedStatement` & `.env`).

---

## 📚 Notions & Compétences Acquises (Moodle)

### 📚 Notions Acquises
- Savoir concevoir une base de données SQL.
- Savoir mettre en œuvre des scripts de création de base de données SQL.
- Savoir mettre en œuvre des scripts de remplissage de base de données SQL.
- Savoir communiquer en Java / PHP avec une base de données SQL.
- Savoir sécuriser le code applicatif d'accès à une base de données.

### 🎯 Compétences Validées
- **Construire une base de données relationnelle à l'aide d'un outil de modélisation.**
- **Construire une base de données relationnelle.**
