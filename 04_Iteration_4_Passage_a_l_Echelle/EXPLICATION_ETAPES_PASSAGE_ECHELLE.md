# 📘 Guide Explicatif Pas à Pas — SQL et Passage à l'Échelle (Itération 4 / Atelier 1)

> [!NOTE]
> Ce guide détaille la méthode, la logique, les objectifs, les commandes et les bonnes pratiques pour réaliser chacune des étapes du module **SQL et Passage à l'Échelle** (7h - Go2Moodle).

---

## 📑 Sommaire des Étapes Moodle

- [1.1 | Passage à l'échelle (~7h Autonomie)](#11--passage-à-léchelle-7h)
  - [Étape 1 : Connaissances — Index (30 min)](#étape-1--connaissances--indexes)
  - [Étape 2 : Connaissances — Types de données (30 min)](#étape-2--connaissances--types)
  - [Étape 3 : Connaissances — Analyse des requêtes avec `EXPLAIN ANALYZE` (30 min)](#étape-3--connaissances--analyse-des-requêtes)
  - [Exercice 1 : Index utiles sur la Base SIRENE (3h)](#exercice-1--créer-une-base-avec-les-unités-légales-et-établissements-sirene)
  - [Exercice 2 : Script entreprises du 74 créées en 2025 (30 min)](#exercice-2--script-des-entreprises-du-74-ouvertes-en-2025)
  - [Exercice 3 : Nettoyage et suppression des index inutiles (30 min)](#exercice-3--suppression-des-indexes-inutiles)
  - [Exercice 4 : Optimisation des types de colonnes (30 min)](#exercice-4--optimisation-des-types-de-colonnes)
  - [Exercice Bonus : Indexation textuelle `FULLTEXT`](#exercice-bonus--indexation-fulltext)
- [📦 Convention de Nommage des Livrables Moodle](#-convention-de-nommage-des-livrables-moodle)

---

# 1.1 | Passage à l'échelle (~7h)

## Étape 1 : Connaissances — Indexes
- **Principe** : Les performances de recherche dépendent directement de la présence des index sur les colonnes des clauses `WHERE`, `JOIN`, `HAVING`, PK et FK.
- **Règles d'or** :
  - Conserver les index en RAM pour éviter les accès disque lents.
  - Prendre en compte la **cardinalité** (indexer un booléen est inutile).
  - Utiliser des **index composites** pour les recherches multi-critères (`WHERE colA = x AND colB = y`).
  - Supprimer les index redondants.

---

## Étape 2 : Connaissances — Types
- **Principe** : Sélectionner le type de plus petite taille (en octets) compatible avec les données métier.
- **Gain** : Économiser des octets sur chaque ligne d'une table à forte volumétrie réduit la taille mémoire RAM et accélère le parcours d'index.

---

## Étape 3 : Connaissances — Analyse des requêtes
- **Outil** : `EXPLAIN ANALYZE <requête SQL>`.
- **Méthode** : Comparer le coût (*cost*) et le temps réel (*actual time*) entre :
  1. Sans index (Full Table Scan - `ALL`).
  2. Avec un mauvais index.
  3. Avec un index sub-optimal.
  4. Avec l'index composite parfait (`ref` / `range`).

---

## Exercice 1 : Base SIRENE avec index utiles ajoutés
- **Contexte** : Formulaire de recherche backend par **SIREN, SIRET, Code Postal, Département, Code Activité NAF**.
- **Actions** :
  - Ajouter un index `UNIQUE` sur `siret` et `siren`.
  - Ajouter un index composite sur `(code_postal, code_activite)`.
  - Ajouter un index sur `code_departement`.
- 📁 **Fichier livré** : `02_exercice1_indexes_sirene.sql`

---

## Exercice 2 : Script des entreprises du 74 ouvertes en 2025
- **Contexte** : Lister les entreprises de la Haute-Savoie ouvertes en 2025.
- **Action** : Créer l'index composite le plus performant possible `(code_departement, date_creation, siren)` et vérifier son usage avec `EXPLAIN ANALYZE`.
- 📁 **Fichier livré** : `03_exercice2_entreprises_74.sql`

---

## Exercice 3 : Suppression des indexes inutiles
- **Contexte** : Base volumineuse ralentie par une sur-indexation.
- **Action** : Analyser les statistiques d'utilisation des index, supprimer les index redondants ou à faible cardinalité pour réduire l'empreinte disque/RAM.
- 📁 **Fichier livré** : `04_exercice3_nettoyage_indexes.sql`

---

## Exercice 4 : Optimisation des types de colonnes
- **Contexte** : Colonnes au type surdimensionné (`VARCHAR(255)` pour un code postal ou `INT` pour un statut).
- **Action** : Écrire les requêtes d'inspection (`MAX(CHAR_LENGTH(...))`) et modifier le schéma (`ALTER TABLE ... MODIFY ...`).
- 📁 **Fichier livré** : `05_exercice4_optimisation_types.sql`

---

## Exercice Bonus : Indexation FULLTEXT
- **Contexte** : Recherche textuelle avancée sur la dénomination sociale.
- **Action** : Créer un index `FULLTEXT` et comparer le temps d'exécution entre `LIKE '%Boulangerie%'` et `MATCH(denomination) AGAINST('+Boulangerie' IN BOOLEAN MODE)`.
- 📁 **Fichier livré** : `06_bonus_fulltext_search.sql`

---

# 📦 Convention de Nommage des Livrables Moodle

Pour rendre vos livrables conformes aux exigences du formateur / Moodle :
```text
[Nom]-[Prénom]-[Site]-Atelier1-[NomLivrable]
Exemple : SOURICHANH-Bernard-Campus-Atelier1-BaseSIRENE.sql
```
