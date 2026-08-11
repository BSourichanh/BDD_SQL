# 🎓 Guide de Compréhension — Itération 4 : Passage à l'Échelle SIRENE & Performance BDD

Ce document résume **tout ce qu'il faut comprendre et maîtriser** pour l'Itération 4 (Passage à l'échelle sur 600 000+ établissements).

---

## 📍 Étape 1 : Le Problème du Passage à l'Échelle (Volumétrie)
- **Ce qu'il faut comprendre** : Lorsqu'une table dépasse plusieurs centaines de milliers de lignes, un `SELECT * FROM etablissements WHERE code_departement = '74'` sans index effectue un **Full Table Scan** (lecture intégrale du disque), ce qui prend plusieurs secondes.

---

## 📍 Étape 2 : L'Optimisation par les Index B-Tree
- **Ce qu'il faut comprendre** : Un index B-Tree est un arbre de recherche équilibré qui stocke les clés et leurs adresses disque.
  - **Création d'un index utile** :
    ```sql
    CREATE INDEX idx_dept ON etablissements(code_departement);
    CREATE INDEX idx_act ON etablissements(code_activite);
    ```
  - **Attention aux index superflus** : Trop d'index ralentissent considérablement les `INSERT` et `UPDATE` et consomment de la RAM inutilement. Il faut supprimer les index inutilisés.

---

## 📍 Étape 3 : L'Analyse du Plan d'Exécution (EXPLAIN ANALYZE)
- **Ce qu'il faut comprendre** : L'outil `EXPLAIN ANALYZE` permet de vérifier quel index est choisi par le moteur SQL et de mesurer le temps d'exécution réel :
  ```sql
  EXPLAIN ANALYZE SELECT * FROM etablissements WHERE code_departement = '74';
  ```
  - **Index Scan (Bien)** : Le moteur accède directement aux lignes via l'index en quelques millisecondes.
  - **Table Scan (Mauvais sur gros volumes)** : Le moteur lit tout le disque.

---

## 📍 Étape 4 : Optimisation des Types de Colonnes SQL
- **Ce qu'il faut comprendre** : Choisir le type le plus ajusté économise des gigaoctets de RAM et de disque :
  - `VARCHAR(255)` pour un code postal -> Remplacer par `CHAR(5)` ou `VARCHAR(10)`.
  - Statut actif/inactif -> Remplacer par `TINYINT(1)` ou `ENUM('ACTIF', 'INACTIF')`.
  - Date sous forme de texte -> Remplacer par `DATE`.

---

## 📍 Étape 5 : Moteur de Recherche Web & API SQL
- **Ce qu'il faut comprendre** : L'application web interroge la BDD via des requêtes dynamiques sécurisées avec filtres multi-critères (SIRET, Nom, Code NAF, Département), réutilisant les index B-Tree pour renvoyer des résultats instantanés.
