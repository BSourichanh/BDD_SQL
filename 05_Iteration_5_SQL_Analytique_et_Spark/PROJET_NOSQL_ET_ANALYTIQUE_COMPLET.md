# Synthèse du Projet — Itération 5 : SQL Analytique, Apache Spark, Parquet & Spring Boot (Java)

**Auteur** : Bernard SOURICHANH  
**Formation** : DEVAA 2028 — Base de Données SQL & Technologies Analytiques  
**Projet** : Traitement et Analyse Decisionnelle de la Base SIRENE (INSEE)  

---

## 🎯 Résumé des Réalisations de l'Itération 5

Dans cette cinquième itération, nous sommes passés des traitements transactionnels (OLTP) aux **traitements analytiques de masse (OLAP)** pour concevoir un **système d'informatique décisionnelle (Business Intelligence) performant**.

### 1. Synthèse Théorique (OLTP vs OLAP)
- **Modèle OLTP** (Transactionnel) : Privilégie l'intégrité, les petites lectures/écritures unitaires et l'usage des index B-Tree.
- **Modèle OLAP** (Analytique) : Privilégie le calcul d'agrégats de masse (`COUNT`, `SUM`, `AVG`), le stockage en colonnes (**Parquet**) et le traitement distribué In-Memory (**Apache Spark & Java Spring Boot**).

### 2. Algorithme MapReduce & Apache Spark
- Implémentation du paradigme **MapReduce** (*Map, Shuffle & Reduce*) pour paralléliser le comptage d'établissements et de sièges sociaux par commune et par département.
- Utilisation des **Datasets Apache Spark (`Dataset<Row>`) In-Memory** stockés en mémoire vive Java pour éviter les E/S disque coûteuses.

---

## 📁 Liste des Livrables Officiels (Conventions Campus)

| Exercice | Livrable Officiel | Description |
| :--- | :--- | :--- |
| **Exercice 1** | `SOURICHANH-Bernard-Campus-Atelier2-BaseReduite.py` | Génération de la base analytique optimisée au format CSV/Parquet par commune. |
| **Exercice 2, 3, 5** | `SOURICHANH-Bernard-Campus-Atelier2-ComptagesAnalytiques.sql` | Requêtes d'agrégation SQL (Comptage par commune, département, Top/Flop 10). |
| **Exercice 4** | `SOURICHANH-Bernard-Campus-Atelier2-ExplicationPerformance.md` | Mémo explicatif du comparatif de performance MySQL (disque/lignes) vs Spark (RAM/colonnes). |
| **Exercice 6** | `spring_spark_dashboard/` | Application Web Decisionnelle Java Spring Boot + Apache Spark (`SparkConfig.java`, `AnalyticsController.java`, `pom.xml`). |

---

## 🌐 Lancement du Dashboard Web Decisionnel Java Spring Boot (Exercice 6)

Pour démarrer l'application Java Spring Boot + Apache Spark :

```bash
cd 05_Iteration_5_SQL_Analytique_et_Spark/spring_spark_dashboard
mvn spring-boot:run
```

Puis accédez à **`http://localhost:8090`** dans votre navigateur pour visualiser :
- 🗺️ La **carte de chaleur de la France** par département.
- 📈 La **Time Series** des créations d'entreprises de 1995 à 2026.
- 📊 Les **Top 10 et Flop 10** des communes et départements français.
- 🏢 Le classement des **10 plus grandes entreprises** par nombre d'établissements.
