# 📦 Projet BDD SQL, NoSQL & SQL Analytique — Obsidian Vault & Guide Général

> [!INFO] **Informations Générales**
> **Module** : BDD SQL DEVAA 2028 (Jour 1, 2, 3, 4 et 5)
> **Apprenant** : Bernard SOURICHANH (Campus Numérique)
> **Description** : Structure épurée et numérotée regroupant les 5 itérations du cours (Conception, Sécurité, NoSQL, Passage à l'échelle SIRENE, SQL Analytique & Apache Spark).

---

## 🗂️ Arborescence Logique du Vault (Itérations 1 à 5)

```text
BDD_SQL/
│
├── 01_Iteration_1_Conception_et_Creation/             <-- ITÉRATION 1 : MCD, MLD, DDL, DML
│   ├── PROJET_BDD_SQL_COMPLET.md                       <-- Synthèse Conception
│   ├── EXPLICATION_ETAPES_PROJET_BDD.md                <-- Guide Pas à Pas
│   ├── Projet_BDD_SQL_Guide_Obsidian.md                <-- Guide Vault Obsidian
│   ├── 01_conventions_nommage.md                       <-- Naming Conventions
│   ├── 02_dictionnaire_donnees.md                      <-- Dictionnaire de Données
│   ├── 03_mcd_mld.md                                   <-- MCD & MLD Merise
│   ├── 04_schema_creation.sql                          <-- Script DDL BDD (6 tables)
│   ├── 05_insertion_donnees.sql                        <-- Script DML Données Test
│   └── test_bdd.py                                     <-- Script de validation SQLite
│
├── 02_Iteration_2_Securisation_et_Privileges/          <-- ITÉRATION 2 : Sécurité & Privilèges SQL
│   ├── Sujet_Officiel_Moodle/                          <-- Sujet officiel Moodle
│   ├── VULNERABILITES_ET_SECURITE_SQL.md               <-- Mémo Injections & BCrypt
│   ├── 06_memo_securite_sql.md                         <-- Synthèse Failles SQL
│   └── 07_patch_securite.sql                           <-- Patch Droits & Privilèges GRANT/REVOKE
│
├── 03_Iteration_3_NoSQL/                              <-- ITÉRATION 3 : Introduction au NoSQL
│   ├── PROJET_NOSQL_COMPLET.md                         <-- Synthèse NoSQL
│   ├── EXPLICATION_ETAPES_NOSQL.md                     <-- Guide Pas à Pas NoSQL
│   ├── 01_memo_cap_theorem.md                          <-- Mémo Théorème CAP
│   ├── 02_mongodb_requetes.js                          <-- Requêtes MongoDB (mflix/movies)
│   ├── 03_neo4j_cypher.cypher                          <-- Requêtes Cypher Neo4j (Pizzas/Movies)
│   └── 04_quiz_game_java_nosql.md                      <-- Application Java Quiz Terminal
│
├── 04_Iteration_4_Passage_a_l_Echelle/                 <-- ITÉRATION 4 : Passage à l'Échelle (SIRENE)
│   ├── PROJET_BDD_SQL_PASSAGE_ECHELLE.md               <-- Synthèse Performance BDD
│   ├── EXPLICATION_ETAPES_PASSAGE_ECHELLE.md           <-- Guide 7h Performance
│   ├── 01_memo_index_et_types.md                       <-- Mémo Index B-Tree & EXPLAIN ANALYZE
│   ├── 02_exercice1_indexes_sirene.sql                 <-- SQL Exercice 1 (Index Utiles)
│   ├── 03_exercice2_entreprises_74.sql                 <-- SQL Exercice 2 (Entreprises 74)
│   ├── 04_exercice3_nettoyage_indexes.sql              <-- SQL Exercice 3 (Nettoyage Index)
│   ├── 05_exercice4_optimisation_types.sql             <-- SQL Exercice 4 (Optimisation Types)
│   ├── 06_bonus_fulltext_search.sql                    <-- SQL Bonus (Recherche FULLTEXT)
│   ├── 07_import_sirene_csv.py                         <-- Importation & Benchmark Python
│   ├── 08_load_data_sirene_mysql.sql                   <-- Importation Native MySQL LOAD DATA
│   └── formulaire_recherche_sirene/                    <-- Application Web & API SQL (Glassmorphism)
│       ├── app.py                                      <-- API Python HTTP sans limitation 50
│       ├── index.html                                  <-- Formulaire HTML (Recherche NAF, Dept, Siret...)
│       └── index.php                                   <-- Version Apache PHP
│
├── 05_Iteration_5_SQL_Analytique_et_Spark/             <-- ITÉRATION 5 : SQL Analytique, Spark & Parquet
│   ├── Sujet_Officiel_Moodle/                          <-- Sujet officiel Moodle
│   ├── PROJET_NOSQL_ET_ANALYTIQUE_COMPLET.md           <-- Synthèse Decisionnelle
│   ├── 01_memo_oltp_vs_olap_spark.md                   <-- Mémo Théorique OLTP/OLAP & MapReduce
│   ├── 03_exercices_2_3_5_requetes_spark_sql.py        <-- Runner de test requêtes SQL analytiques
│   ├── SOURICHANH-Bernard-Campus-Atelier2-BaseReduite.py           <-- Livrable Ex 1 (Base réduite Parquet/CSV)
│   ├── SOURICHANH-Bernard-Campus-Atelier2-ComptagesAnalytiques.sql <-- Livrable Ex 2, 3, 5 (Requêtes SQL)
│   ├── SOURICHANH-Bernard-Campus-Atelier2-ExplicationPerformance.md <-- Livrable Ex 4 (MySQL vs Spark)
│   ├── SOURICHANH-Bernard-Campus-Atelier2-DashboardSpark.py        <-- Livrable Ex 6 (API & Cache In-Memory)
│   └── static/index.html                                           <-- Dashboard UI (Plotly.js Heatmap)
│
├── 06_Donnees_CSV/                                    <-- Fichiers CSV INSEE SIRENE
│   ├── StockUniteLegale_utf8.csv
│   └── StockEtablissement_utf8.csv
│
├── 07_Scripts_Global_et_Docker/                        <-- Automation & Docker
│   ├── test_projet_global.py                          <-- Runner Master Validation Globale
│   ├── run_all_docker.sh                               <-- Runner Docker Global
│   └── docker-compose.yml
│
├── docker-compose.yml                                  <-- Docker Compose racine
└── README.md                                          <-- Le présent fichier
```

---

## 🛠️ Exécution & Test des Applications Web

### 1. Formulaire de Recherche SIRENE (Itération 4)
- **Lancement** :
  ```bash
  python3 04_Iteration_4_Passage_a_l_Echelle/formulaire_recherche_sirene/app.py
  ```
- **Accès Web** : **`http://localhost:8000`** ou **`http://localhost:8080`**

### 2. Dashboard Analytique Spark Decisionnel (Itération 5)
- **Lancement** :
  ```bash
  python3 05_Iteration_5_SQL_Analytique_et_Spark/SOURICHANH-Bernard-Campus-Atelier2-DashboardSpark.py
  ```
- **Accès Web** : **`http://localhost:8090`**

---

## 📊 Synthèse des Livrables Officiels (Conventions Campus)

| Itération | Fichier Livrable | Description |
| :--- | :--- | :--- |
| **Atelier 1 (Itération 4)** | `SOURICHANH-Bernard-Campus-Atelier1-BaseSIRENE.sql` | Importation et création de la base SIRENE sur MySQL. |
| **Atelier 1 (Itération 4)** | `SOURICHANH-Bernard-Campus-Atelier1-Entreprises74.sql` | Requête d'extraction des établissements du 74. |
| **Atelier 1 (Itération 4)** | `SOURICHANH-Bernard-Campus-Atelier1-IndexesInutiles.sql` | Nettoyage des index superflus B-Tree. |
| **Atelier 1 (Itération 4)** | `SOURICHANH-Bernard-Campus-Atelier1-OptimisationTypes.sql` | Optimisation des types SQL (VARCHAR -> CHAR/INT/ENUM). |
| **Atelier 2 (Itération 5)** | `SOURICHANH-Bernard-Campus-Atelier2-BaseReduite.py` | Génération de la base analytique réduite par commune (Parquet/CSV). |
| **Atelier 2 (Itération 5)** | `SOURICHANH-Bernard-Campus-Atelier2-ComptagesAnalytiques.sql` | Requêtes d'agrégation SQL (Comptages communes, depts, Top/Flop 10). |
| **Atelier 2 (Itération 5)** | `SOURICHANH-Bernard-Campus-Atelier2-ExplicationPerformance.md` | Mémo de performance (MySQL vs Apache Spark). |
| **Atelier 2 (Itération 5)** | `SOURICHANH-Bernard-Campus-Atelier2-DashboardSpark.py` | Dashboard Web Decisionnel PySpark In-Memory & Plotly.js. |
