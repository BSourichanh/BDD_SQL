# 🛠️ GUIDE ÉTAPE PAR ÉTAPE PAS À PAS — ITÉRATION 6 (RAG & VECTOR SEARCH)

Ce guide vous explique **explicitement et étape par étape** toutes les manipulations à réaliser pour exécuter, tester et valider l'**Itération 6**.

---

## 📍 ÉTAPE 1 : Générer la Base de Données Vectorielle BODACC (Embeddings 384d)

1. Ouvrez votre terminal dans le dossier du projet :
   ```bash
   cd /home/user/Documents/Cours/BDD_SQL/
   ```
2. Lancez le générateur d'embeddings vectoriels sur les entreprises réelles SIRENE :
   ```bash
   python3 06_Iteration_6_SQL_et_IA_Vectorielle/SOURICHANH-Bernard-Campus-Atelier2-GenerateurEmbeddingsBODACC.py --full
   ```
3. **Résultat attendu** :
   - Le script lit le fichier `StockEtablissement_utf8.csv` avec la barre de progression blanche solide `█`.
   - Il produit le fichier vectoriel **`06_Iteration_6_SQL_et_IA_Vectorielle/bodacc_vector_dataset.json` (388 Mo, 100 000 établissements réels)** en environ 30 secondes.

---

## 📍 ÉTAPE 2 : Déployer et Charger le Schéma SQL Vectoriel MariaDB 11

1. Vérifiez que la table SQL vectorielle est définie avec la colonne `VECTOR(384)` dans :
   `06_Iteration_6_SQL_et_IA_Vectorielle/SOURICHANH-Bernard-Campus-Atelier2-BodaccVectorSchema.sql`
2. Schéma DDL MariaDB 11 utilisé :
   ```sql
   CREATE TABLE IF NOT EXISTS bodacc_jugements (
       id_annonce INT PRIMARY KEY AUTO_INCREMENT,
       siren VARCHAR(9) NOT NULL,
       siret VARCHAR(14) NOT NULL,
       denomination VARCHAR(255) NOT NULL,
       type_procedure VARCHAR(100) NOT NULL,
       tribunal VARCHAR(150) NOT NULL,
       detail_jugement TEXT NOT NULL,
       vector_embedding VECTOR(384) NOT NULL
   );
   ```

---

## 📍 ÉTAPE 3 : Redémarrer le Serveur Docker Spring Boot

Pour recharger le nouveau dataset vectoriel de 388 Mo en mémoire vive Java :
```bash
sudo docker restart docker_spring_spark_dashboard
```

---

## 📍 ÉTAPE 4 : Tester et Manipuler le Moteur RAG sur le Site Web

1. Ouvrez votre navigateur sur **[http://localhost:8090](http://localhost:8090)** (`Ctrl + F5`).
2. Cliquez sur le **3ème Onglet : `🤖 Recherche Sémantique IA (RAG BODACC)`**.
3. **Faire un test de recherche sémantique** :
   - Tapez par exemple : `"liquidation judiciaire pour impayés à marseille"`
   - Ou cliquez sur un bouton d'exemple : `[🥖 Boulangerie en redressement]`.
4. Cliquez sur **"🧠 Calculer Vector Search & RAG"**.
5. **Résultat attendu** :
   - Le tableau affiche instantanément les entreprises réelles avec leur **score de similarité en %** (ex: `94.8 %`), le type de procédure, le tribunal et le détail du jugement !

---

## 📍 ÉTAPE 5 : Vérifier le Livrable Officiel pour Moodle

Vérifiez la présence du document théorique rédigé pour Moodle :
📄 **`06_Iteration_6_SQL_et_IA_Vectorielle/SOURICHANH-Bernard-Campus-Atelier2-RAG_ExplicationVectorielle.md`**

Ce document contient les réponses aux questions de cours sur :
- La différence entre BDD relationnelle et BDD vectorielle.
- Le rôle des Embeddings 384d et de la Distance Cosinus.
- Les contraintes matérielles (RAM/CPU/GPU).
- Le pipeline RAG pour alimenter un modèle LLM sans hallucination.
