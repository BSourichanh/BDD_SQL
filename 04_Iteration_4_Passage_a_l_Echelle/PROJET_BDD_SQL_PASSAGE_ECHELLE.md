# 🚀 Projet BDD SQL — Passage à l'Échelle & Performance (Itération 4 / Atelier 1)

> [!INFO] **Informations Générales**
> **Module** : BDD SQL DEVAA2028 — Itération 4 : SQL et Passage à l'Échelle
> **Durée** : 7 heures en autonomie
> **Jeu de données réel (CSV)** : Base SIRENE (INSEE / data.gouv.fr)
> - `04_Donnees_CSV/StockUniteLegale_utf8.csv` (Données des entreprises / Unités Légales)
> - `04_Donnees_CSV/StockEtablissement_utf8.csv` (Données des établissements / Sièges & Succursales)
> **Objectifs** : Maîtriser l'indexation SQL sur gros volumes CSV, l'optimisation des types de données et l'analyse avec `EXPLAIN ANALYZE`.

---

## 📑 Sommaire

- [1. Présentation & Jeu de Données CSV SIRENE](#1-présentation--jeu-de-données-csv-sirene)
- [2. Synthèse Théorique (Indexation, Types, EXPLAIN ANALYZE)](#2-synthèse-théorique)
- [3. Exercice 1 : Ajout des Index Utiles (Base SIRENE)](#3-exercice-1--ajout-des-index-utiles-base-sirene)
- [4. Exercice 2 : Recherche Optimisée Entreprises du 74 (2025)](#4-exercice-2--recherche-optimisée-entreprises-du-74-2025)
- [5. Exercice 3 : Nettoyage et Suppression des Index Inutiles](#5-exercice-3--nettoyage-et-suppression-des-index-inutiles)
- [6. Exercice 4 : Optimisation des Types de Colonnes](#6-exercice-4--optimisation-des-types-de-colonnes)
- [7. Exercice Bonus : Recherche Textuelle FULLTEXT](#7-exercice-bonus--recherche-textuelle-fulltext)
- [8. Script d'Importation Automatique CSV (`07_import_sirene_csv.py`)](#8-script-dimportation-automatique-csv-07_import_sirene_csvpy)
- [9. Checklist des Livrables Moodle](#9-checklist-des-livrables-moodle)

---

# 1. Présentation & Jeu de Données CSV SIRENE

Cette itération traite de l'optimisation des performances d'une base de données relationnelle MySQL/SQLite soumise au passage à l'échelle (*scaling*) sur de très fortes volumétries importées depuis les deux fichiers CSV officiels de l'INSEE.

---

# 2. Synthèse Théorique

### ⚡ Indexation B-Tree & Performance
- Un index réduit la complexité de recherche de $\mathcal{O}(N)$ (Full Table Scan) à $\mathcal{O}(\log N)$ (Arbre équilibré).
- **Index Composite** : L'ordre des colonnes doit suivre la sélectivité de la clause `WHERE`.

---

# 3. Exercice 1 : Ajout des Index Utiles (Base SIRENE)

```sql
USE base_sirene;

-- Indexation unique pour les identifiants SIREN / SIRET
CREATE UNIQUE INDEX idx_unites_legales_siren ON unites_legales(siren);
CREATE UNIQUE INDEX idx_etablissements_siret ON etablissements(siret);

-- Index composite pour la recherche par Code Postal + Code Activité
CREATE INDEX idx_etablissements_cp_activite ON etablissements(code_postal, code_activite);
```

---

# 4. Exercice 2 : Recherche Optimisée Entreprises du 74 (2025)

```sql
-- Index composite recouvrant (Covering Index)
CREATE INDEX idx_etab_dept_date_creation ON etablissements(code_departement, date_creation, siren);

-- Requête de recherche optimisée
EXPLAIN ANALYZE 
SELECT DISTINCT ul.siren, ul.denomination, e.code_postal, e.date_creation
FROM unites_legales ul
JOIN etablissements e ON ul.siren = e.siren
WHERE e.code_departement = '74' AND e.date_creation >= '2025-01-01';
```

---

# 5. Exercice 3 : Nettoyage et Suppression des Index Inutiles

```sql
-- Détection des index jamais utilisés dans performance_schema
SELECT OBJECT_NAME, INDEX_NAME 
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE count_star = 0 AND object_schema = 'base_sirene';

-- Suppression des index inutiles / redondants
DROP INDEX idx_etablissements_cp_simple ON etablissements;
```

---

# 6. Exercice 4 : Optimisation des Types de Colonnes

```sql
-- Modification du schéma pour compacter la mémoire
ALTER TABLE etablissements MODIFY code_postal CHAR(5) NOT NULL;
ALTER TABLE etablissements MODIFY code_departement VARCHAR(3) NOT NULL;
ALTER TABLE etablissements MODIFY est_actif TINYINT(1) NOT NULL DEFAULT 1;
```

---

# 7. Exercice Bonus : Recherche Textuelle FULLTEXT

```sql
-- Ajout de l'index FULLTEXT sur la dénomination
ALTER TABLE unites_legales ADD FULLTEXT INDEX ft_idx_denomination(denomination);

-- Recherche haute performance
EXPLAIN ANALYZE 
SELECT siren, denomination 
FROM unites_legales 
WHERE MATCH(denomination) AGAINST('+Boulangerie' IN BOOLEAN MODE);
```

---

# 8. Script d'Importation Automatique CSV (`07_import_sirene_csv.py`)

```bash
python3 03_Iteration_4_Passage_a_l_Echelle/dossier_performance/07_import_sirene_csv.py
```

---

# 9. Checklist des Livrables Moodle

- [x] **Base SIRENE avec index utiles ajoutés** (`02_exercice1_indexes_sirene.sql`)
- [x] **Script entreprises du 74 en 2025 avec index optimisé** (`03_exercice2_entreprises_74.sql`)
- [x] **Base allégée après suppression des index inutiles** (`04_exercice3_nettoyage_indexes.sql`)
- [x] **Types de colonnes optimisés avec requêtes d'analyse** (`05_exercice4_optimisation_types.sql`)
- [x] **Indexation textuelle FULLTEXT benchmarkée** (`06_bonus_fulltext_search.sql`)
- [x] **Script d'importation et d'indexation des CSV réels** (`07_import_sirene_csv.py`)
