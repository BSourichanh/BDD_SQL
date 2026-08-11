# 🎓 Guide de Compréhension — Itération 3 : Introduction au NoSQL

Ce document résume **tout ce qu'il faut comprendre et maîtriser** pour l'Itération 3 (Bases NoSQL Documentaires & Graphes).

---

## 📍 Étape 1 : Le Théorème CAP (Le Socle Théorique)
- **Ce qu'il faut comprendre** : Dans un système distribué, il est impossible de garantir simultanément les 3 propriétés du Théorème CAP :
  1. **C (Consistency / Cohérence)** : Tous les nœuds voient exactement les mêmes données au même instant.
  2. **A (Availability / Disponibilité)** : Chaque requête reçoit une réponse (succès ou échec).
  3. **P (Partition Tolerance / Tolérance au morcellement)** : Le système continue de fonctionner malgré des pannes réseau.
- **Choix d'architecture** :
  - **Bases CP (ex: MongoDB, HBase)** : Privilégient la cohérence lors de coupures réseau.
  - **Bases AP (ex: Cassandra, CouchDB)** : Privilégient la disponibilité absolue.

---

## 📍 Étape 2 : Bases Documentaires avec MongoDB
- **Ce qu'il faut comprendre** :
  - Les données sont stockées au format **JSON / BSON** sous forme de documents flexibles sans schéma fixe (*Schema-less*).
  - **Requêtes & Agrégations** :
    ```javascript
    // Recherche filtrée
    db.movies.find({ year: { $gte: 2000 }, "imdb.rating": { $gt: 8.0 } });

    // Pipeline d'Agrégation ($match -> $group -> $sort)
    db.movies.aggregate([
      { $match: { genres: "Action" } },
      { $group: { _id: "$year", totalMovies: { $sum: 1 }, avgRating: { $avg: "$imdb.rating" } } },
      { $sort: { avgRating: -1 } }
    ]);
    ```

---

## 📍 Étape 3 : Bases Orientées Graphes avec Neo4j (Cypher)
- **Ce qu'il faut comprendre** :
  - Idéal pour les réseaux sociaux, recommandations, cartographies et trajets.
  - Modèle basé sur des **Nœuds** (Entities `(:Person)`), des **Relations** (`-[:LIKES]->`) et des **Propriétés**.
  - **Langage Cypher** :
    ```cypher
    // Créer un nœud et une relation
    CREATE (p:Person {name: 'Bernard'})-[:PREFERS]->(pizza:Food {name: 'Pizza Napolitaine'});

    // Pattern Matching (Recherche de connexions)
    MATCH (p:Person)-[:PREFERS]->(f:Food)
    RETURN p.name, f.name;
    ```
