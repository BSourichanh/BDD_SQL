# 🧠 ITÉRATION 6 : SQL ET BASE DE DONNÉES POUR L'IA (RAG & VECTOR SEARCH)

## 📌 Qu'est-ce que l'Itération 6 ?
L'**Itération 6** introduit les **Bases de Données Vectorielles** et l'architecture **RAG (Retrieval Augmented Generation)**. L'objectif est d'enrichir la base d'entreprises SIRENE avec les annonces légales de procédures collectives du **BODACC** (Bulletins Officiels des Annonces Civiles et Commerciales) sous forme de **Vecteurs (Embeddings 384 dimensions)**.

---

## 🎯 Notions Clés à Maîtriser

### 1. Qu'est-ce qu'un Vector Embedding ?
Un *embedding* est une représentation numérique (une liste de nombres flottants `[0.024, -0.158, ..., 0.891]`) produite par un réseau de neurones Transformer (`all-MiniLM-L6-v2`).  
Deux textes qui ont un **sens proche** (ex: *"boulangerie en faillite"* et *"procédure de liquidation judiciaire boulangerie"*) auront des vecteurs **très proches dans l'espace vectoriel** (distance cosinus proche de 0, similarité proche de 100%).

### 2. Le RAG (Retrieval Augmented Generation)
Le RAG permet de donner à une IA (LLM) l'accès à des données privées ou récentes stockées dans une base de données :
```text
[Requête Utilisateur] ➡️ [Vectorisation Requête] ➡️ [Recherche Cosinus SQL/Vector] ➡️ [Contexte Injecté dans l'IA] ➡️ [Réponse Précise]
```

### 3. Les Technologies Vectorielles (MariaDB 11 VECTOR, PgVector, ChromaDB)
- **MariaDB 11 / Vector** : Stocke le vecteur `VECTOR(384)` directement dans la table SQL aux côtés des colonnes `SIREN`, `DATE`, `TEXTE`.
- **PgVector (PostgreSQL)** : Extension SQL permettant la création d'index HNSW / IVF.
- **ChromaDB / Qdrant** : BDD purement vectorielle orientée RAM.

---

## 📂 Livrables Officiels de l'Itération 6
- `SOURICHANH-Bernard-Campus-Atelier2-BodaccVectorSchema.sql` : DDL SQL de la table vectorielle.
- `SOURICHANH-Bernard-Campus-Atelier2-GenerateurEmbeddingsBODACC.py` : Générateur d'embeddings BODACC 384d.
- `SOURICHANH-Bernard-Campus-Atelier2-RAG_ExplicationVectorielle.md` : Explications théoriques RAG & Vector Search.
- `spring_spark_dashboard/` : Application Web Java Spring Boot Unifiée (IT4 + IT5 + IT6).
