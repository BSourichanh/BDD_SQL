# 🎓 Guide de Compréhension — Itération 5 : SQL Analytique, Apache Spark & Parquet

Ce document résume **tout ce qu'il faut comprendre et maîtriser** pour l'Itération 5 (Informatique Décisionnelle & OLAP).

---

## 📍 Étape 1 : Différence OLTP vs OLAP (Le Concept Clé)
- **OLTP (Transactionnel)** : Gestion des opérations en temps réel (*ex: passer une commande*). Requêtes unitaires très rapides, modèles normalisés, usage intensif des index B-Tree.
- **OLAP (Analytique / Décisionnel)** : Analyse globale de masse (*ex: calculer le nombre d'entreprises par département sur 10 ans*). Agrégations de masse (`SUM`, `COUNT`, `AVG`, `GROUP BY`), stockage par colonnes (Parquet) et calcul In-Memory (Spark).

---

## 📍 Étape 2 : Réduction de Base & Format Parquet (Exercice 1)
- **Problème** : Un fichier CSV brut SIRENE fait 10 Go. Recharger 10 Go à chaque calcul analytique est irréaliste.
- **Solution (Base Réduite)** : On pré-agrège les données par commune dans une base dédiée (`sirene_analytique_commune.csv` de 716 Ko).
- **Format Parquet (Stockage Colonnes)** : Stocke les données par colonnes (au lieu de lignes). Si la requête n'a besoin que du `code_postal`, Spark ne lit que cette colonne sur disque.

---

## 📍 Étape 3 : Requêtes SQL d'Agrégation (Exercices 2, 3 & 5)
- **`GROUP BY`** : Fusionne toutes les lignes de la même commune ou département.
- **`COUNT(*)`** : Compte les établissements par groupe.
- **`SUM(CASE WHEN etablissementSiege = 'true' THEN 1 ELSE 0 END)`** : Compte sélectivement les sièges sociaux.
- **`ORDER BY ... DESC/ASC LIMIT 10`** : Extrait les **Top 10** et **Flop 10**.

---

## 📍 Étape 4 : Performance MySQL vs Apache Spark (Exercice 4)
- **MySQL** : Stocke sur disque par lignes, mono-thread par requête. Lent sur gros volumes analytiques.
- **Apache Spark** : Stocke en **mémoire RAM (In-Memory)**, lit le format colonnes Parquet, et distribue le calcul en parallèle sur **tous les cœurs processeurs**.

---

## 📍 Étape 5 : L'Algorithme MapReduce (Map, Shuffle, Reduce)
1. **Map** : Découpe les données en couples `(Commune, 1)`.
2. **Shuffle** : Regroupe toutes les valeurs de la même commune sur le même nœud de calcul.
3. **Reduce** : Additionne tous les `1` pour calculer le résultat final.

---

## 📍 Étape 6 : Dashboard Décisionnel Web (Exercice 6)
- **Architecture In-Memory** : Le serveur Python/Spark charge les datasets une seule fois au démarrage dans la mémoire RAM.
- **Visualisation Plotly.js** : Restitution graphique interactive sur **`http://localhost:8090`** (Carte de chaleur de la France, Time Series, Top/Flop).
