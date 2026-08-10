# 📦 Projet BDD SQL & NoSQL — Arborescence Optimisée du Projet

> [!INFO] **Informations Générales**
> **Module** : BDD SQL DEVAA2028 (Jour 1, 2, 3 et 4)
> **Description** : Structure propre et numérotée regroupant les 4 itérations du cours sans sous-dossiers imbriqués.

---

## 🗂️ Arborescence Logique du Projet

```text
BDD_SQL/
│
├── 01_Iteration_1_Conception_et_Creation/             <-- ITÉRATION 1 : MCD, MLD, DDL, DML
│   ├── PROJET_BDD_SQL_COMPLET.md                       <-- Synthèse Conception
│   ├── EXPLICATION_ETAPES_PROJET_BDD.md                <-- Guide Pas à Pas
│   ├── 01_conventions_nommage.md                       <-- Conventions Naming
│   ├── 02_dictionnaire_donnees.md                      <-- Dictionnaire de Données
│   ├── 03_mcd_mld.md                                   <-- MCD & MLD Merise
│   ├── 04_schema_creation.sql                          <-- Script DDL BDD (6 tables)
│   ├── 05_insertion_donnees.sql                        <-- Script DML Données Test
│   └── test_bdd.py                                     <-- Script de validation SQLite
│
├── 02_Iteration_2_Securisation_et_Privileges/          <-- ITÉRATION 2 : Sécurité SQL
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
│   ├── SOURICHANH-Bernard-Campus-Atelier1-BaseSIRENE.sql
│   ├── SOURICHANH-Bernard-Campus-Atelier1-Entreprises74.sql
│   ├── SOURICHANH-Bernard-Campus-Atelier1-IndexesInutiles.sql
│   ├── SOURICHANH-Bernard-Campus-Atelier1-OptimisationTypes.sql
│   ├── import_sirene_to_docker.sh                      <-- Automation Docker 1-clic SIRENE
│   └── test_sql_performance.py                         <-- Benchmark de performance
│
├── 05_Donnees_CSV/                                    <-- Fichiers CSV INSEE SIRENE
│   ├── StockUniteLegale_utf8.csv
│   └── StockEtablissement_utf8.csv
│
├── 06_Scripts_Global_et_Docker/                        <-- Automation & Docker
│   ├── test_projet_global.py                          <-- Runner Master Validation Globale
│   ├── run_all_docker.sh                               <-- Runner Docker Global
│   ├── docker-compose.yml
│   └── www/
│
├── docker-compose.yml                                  <-- Docker Compose racine
└── README.md                                          <-- Le présent fichier
```

---

## 🛠️ Exécution et Validation

1. **Validation Dédiée Itération 4 (1-clic)** :
   ```bash
   python3 04_Iteration_4_Passage_a_l_Echelle/07_import_sirene_csv.py
   ```

2. **Validation Globale (Toutes les Itérations 1 à 4)** :
   ```bash
   python3 06_Scripts_Global_et_Docker/test_projet_global.py
   ```
