# Mémo Théorique : OLTP vs OLAP, Algorithme MapReduce & Apache Spark

## 1. Différence Fondamentale : Transactionnel (OLTP) vs Analytique (OLAP)

| Critère | Transactionnel (OLTP) | Analytique (OLAP) |
| :--- | :--- | :--- |
| **Objectif** | Gestion des opérations quotidiennes en temps réel | Analyse décisionnelle, Dashboards & Business Intelligence |
| **Opérations SQL** | `INSERT`, `UPDATE`, `DELETE`, `SELECT` unitaire sur clé | `SELECT` de masse avec `GROUP BY`, `SUM`, `COUNT`, `AVG` |
| **Schéma BDD** | Modèle fortement normalisé (1NF, 2NF, 3NF) | Schéma en Étoile (Star Schema) ou en Flocon (Snowflake) |
| **Rôle des Index** | **Essentiel** (Index B-Tree pour accélération par clé) | **Inutile / Limité** (Obligation de balayer toute la table) |
| **Temps de réponse** | < 10 millisecondes | De quelques secondes à plusieurs minutes |
| **Volume de stockage** | Moins de quelques Go | Téraoctets (To) à Pétaoctets (Po) |
| **Exemples** | Paiement par carte bancaire, gestion des stocks | Analyse des ventes par département, tendance sur 5 ans |

---

## 2. Pourquoi les Index SQL B-Tree ne sont pas utiles en Analytique ?

En mode transactionnel (OLTP), l'index B-Tree permet de sauter directement à un enregistrement précis sans lire le reste du disque.  
En analytique (OLAP), une requête cherche à calculer une statistique sur **l'intégralité ou une très grande partie des données** (ex: *Calculer le nombre total d'entreprises par département*).

- Pour réaliser ce calcul, le SGDB est **obligé de parcourir chaque ligne**.
- L'utilisation d'un index imposerait des accès aléatoires en mémoire/disque supplémentaires, ce qui serait **plus lent** qu'un balayage séquentiel complet de la table (*Table Scan*).
- C'est pourquoi l'analytique s'appuie sur le **stockage orienté colonnes (ex: Parquet)** et le **calcul distribué In-Memory (ex: Apache Spark)**.

---

## 3. L'Algorithme MapReduce & Apache Spark

### Principe de MapReduce
Le modèle MapReduce permet de paralléliser les agrégations complexes sur de grands volumes de données distribuées sur plusieurs serveurs :

1. **Map (Mapping)** : Chaque worker lit un lot de données et émet des couples `(clé, valeur)` (ex: `("74000", 1)`).
2. **Shuffle & Sort** : Les données sont regroupées et triées par clé à travers le réseau afin que toutes les valeurs associées à une même clé arrivent sur le même nœud.
3. **Reduce** : La fonction d'agrégation combine les valeurs (ex: additionne tous les `1` pour la clé `"74000"`).

### Apache Spark & Stockage en Fichiers Parquet
- **Apache Spark** est un moteur open-source de calcul distribué In-Memory 100x plus rapide qu me Hadoop MapReduce traditionnel car il évite les écritures intermédiaires sur disque.
- **Format Parquet** : Format de stockage en colonnes hautement compressé. Au lieu de lire des lignes complètes de 50 colonnes, Spark lit uniquement la colonne `code_postal` et `code_activite`, divisant les E/S disque par 20.
