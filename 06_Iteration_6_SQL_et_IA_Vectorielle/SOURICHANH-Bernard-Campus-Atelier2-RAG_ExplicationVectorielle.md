# LIVRABLE ITÉRATION 6 — RÉPONSES AUX QUESTIONS THÉORIQUES RAG & VECTOR SEARCH
**Convention** : `SOURICHANH-Bernard-Campus-Atelier2-RAG_ExplicationVectorielle.md`

---

## 1. Différence entre Données Structurées et Non Structurées
- **Données Structurées** : Données tabulaires définies par des types stricts (`INTEGER`, `VARCHAR`, `DATE`). Exemple: SIREN `104062153`, Département `75`, Code NAF `10.71C`.
- **Données Non Structurées** : Textes libres de jugements, comptes-rendus juridiques du BODACC, descriptions d'entreprises. Elles ne peuvent pas être filtrées par un simple `=`.

---

## 2. Qu'est-ce qu'un Vector Embedding (384 dimensions) ?
Un vector embedding est une projection mathématique d'un texte dans un espace vectoriel à $N$ dimensions (384 pour le modèle `all-MiniLM-L6-v2`).  
La distance entre deux vecteurs mesure la **similarité sémantique** :
$$\text{Similarité Cosinus}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

---

## 3. Comparatif Hardware & Technologies Vectorielles

| Technologie | Stockage des Vecteurs | Type d'Index | Coût RAM / Hardware | Utilisation Idéale |
| :--- | :--- | :--- | :--- | :--- |
| **ChromaDB / Qdrant** | 100% en RAM | HNSW in-memory | **Élevé** (Toute la BDD doit tenir en RAM) | Prototypage rapide, petits volumes |
| **MariaDB 11 / Vector** | Disque + Cache RAM | Index Vector SQL | **Optimisé** (Seul l'index est en RAM) | Applications SQL hybrides d'entreprise |
| **PgVector (PostgreSQL)** | Disque + Cache RAM | HNSW / IVFflat | **Optimisé** (Seul l'index est en RAM) | Écosystème PostgreSQL robuste |

---

## 4. Pourquoi ChromaDB coûte plus cher dans le Cloud à volume égal ?
ChromaDB conserve l'intégralité des vecteurs et métadonnées directement dans la mémoire vive (RAM). Comme la mémoire RAM coûte entre **5 et 10 fois plus cher au Gigaoctet** que le stockage disque SSD NVMe dans le Cloud (AWS/GCP/Azure), héberger des millions de vecteurs sur ChromaDB revient nettement plus cher que sur une base SQL comme MariaDB 11 ou PgVector qui n'utilise la RAM que pour les index de recherche.
