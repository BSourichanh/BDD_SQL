# Livrable Atelier 2 — Explication des Performances (MySQL vs Spark & Commune vs Établissement)

**Auteur** : Bernard SOURICHANH  
**Formation** : DEVAA 2028 — BDD SQL & Technologies Analytiques  

---

## 1. Différence de Performance entre MySQL (OLTP) et Apache Spark (OLAP)

### Pourquoi MySQL ralenti sur l'analytique de masse :
1. **Stockage Orienté Lignes (Row-Oriented)** :  
   MySQL stocke les données ligne par ligne sur le disque. Lorsqu'une requête effectue `SELECT count(*), code_postal FROM etablissements GROUP BY code_postal;`, MySQL est contraint de charger en mémoire la totalité des octets de chaque ligne (nom, adresse, effectifs, date de création...), même s'il n'a besoin que du `code_postal`.
2. **Exécution Mono-Thread par Requête** :  
   MySQL traite chaque requête SQL sur un seul cœur processeur (thread unique par connexion).
3. **Accès Disque vs RAM** :  
   Les données MySQL résident principalement sur le disque dur / SSD. Même avec le tampon `innodb_buffer_pool`, les lectures séquentielles volumineuses monopolisent le disque.

### Pourquoi Apache Spark est extrêmement rapide en Analytique :
1. **Stockage en Colonnes Parquet (Column-Oriented)** :  
   Le format **Parquet** sépare les colonnes. Pour compter par commune, Spark ne lit **que la colonne `commune`**, ignorant 95% du volume du fichier sur disque !
2. **Calcul Distribué & Multi-Threading (In-Memory)** :  
   Spark découpe les fichiers en blocs (*partitions*) et exécute les calculs en parallèle sur tous les cœurs processeurs disponibles de la machine (ou du cluster).
3. **Exécution In-Memory (RAM)** :  
   Une fois le dataset chargé en mémoire sous forme de `Dataset` / `DataFrame` Spark, les agrégations complexes s'exécutent en quelques millisecondes sans aucun accès disque.

---

## 2. Différence entre le Comptage par Commune et par Établissement

| Critère | Comptage par Commune | Comptage par Établissement |
| :--- | :--- | :--- |
| **Niveau d'Agrégation** | **Global / Macroscopique** (`GROUP BY commune`) | **Détaillé / Microscopique** (Ligne unitaire par SIRET) |
| **Cardinalité de Sortie** | Faible (~35 000 communes en France) | Trés élevée (Plus de 35 millions d'établissements) |
| **Consommation Mémoire** | Réduite (Petite table d'agrégat) | Maximale (Nécessite le stockage de toutes les lignes) |
| **Usage Métier** | Décisionnel : Cartes de chaleur, densité économique territoriale | Opérationnel : Fiche entreprise, facturation, contrôle légal |

- **Le comptage par commune** réduit le volume de données de plusieurs millions de lignes à seulement 35 000 lignes agrégées. C'est l'essence même de l'analytique OLAP.
- **Le comptage par établissement** traite chaque point d'activité individuel (siège social ou secondaire).
