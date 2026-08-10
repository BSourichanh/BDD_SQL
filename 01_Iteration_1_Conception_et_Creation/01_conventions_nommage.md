# 📜 01 — Conventions de Nommage et Règles de Structure

> [!NOTE]
> Ce document définit les normes et conventions adoptées pour la modélisation et l'implémentation de la base de données relationnelle du projet de gestion de livraison de colis en points relais.

---

## 1. Conventions Générales

- **Langue** : Français (termes métier clairs et compréhensibles par l'équipe et le client).
- **Casse** : `snake_case` (lettres minuscules avec des tirets du bas `_` pour séparer les mots).
- **Jeu de caractères** : `utf8mb4` avec la collation `utf8mb4_unicode_ci` (gestion complète des accents et émojis si nécessaire).
- **Mots réservés SQL** : Éviter d'utiliser des mots clés SQL réservés (`date`, `user`, `order`, `status`, `group`, etc.) comme nom de colonne sans préfixe ou suffixe qualificatif.

---

## 2. Nommage des Tables

- **Format** : Nom commun au **pluriel** en `snake_case`.
- **Exemples** :
  - `particuliers` (et non `particulier` ou `Particulier`)
  - `transporteurs`
  - `clients`
  - `missions`
  - `colis`
  - `historique_statuts_colis`

- **Tables d'association (N à N)** : Nom combinant les deux entités concernées au pluriel ou au singulier explicite.
  - Exemple : `missions` (relie `particuliers` et `transporteurs`).

---

## 3. Nommage des Attributs & Colonnes

- **Format** : `snake_case` au **singulier**.
- **Clés Primaires (PK)** : `id_<nom_table_singulier>`
  - Exemples : `id_particulier`, `id_transporteur`, `id_colis`, `id_client`.
  - Type : `INT` ou `BIGINT` avec `AUTO_INCREMENT`.

- **Clés Étrangères (FK)** : `id_<nom_entite_cible_singulier>`
  - Exemples : `id_transporteur` dans la table `missions`, `id_point_relais` dans la table `colis`.
  - Type : Exactement le même type SQL que la clé primaire référencée (`INT`).

- **Dates et Horodatages** : Préfixés par `date_` ou `created_at` / `updated_at`.
  - Exemples : `date_inscription`, `date_debut_mission`, `date_depot`, `date_retrait`.

- **Booléens & Enums** :
  - Booléens préfixés par `est_` ou `est_actif`. Exemple : `est_actif`, `est_fragile`.
  - Énumérations stockées en `VARCHAR(30)` ou `ENUM(...)` avec des constantes en MAJUSCULES (ex: `EN_COURS_LIVRAISON`, `AU_POINT_RELAIS`, `RETIRE`).

---

## 4. Normalisation & Contraintes de Sécurité

1. **Intégrité Référentielle** : Toutes les clés étrangères doivent comporter une contrainte `FOREIGN KEY ... REFERENCES ... ON DELETE RESTRICT ON UPDATE CASCADE` (ou `ON DELETE SET NULL` selon le cas d'usage).
2. **Non-Nullité** : Ajouter `NOT NULL` sur tous les champs obligatoires.
3. **Unicité** : Ajouter des contraintes `UNIQUE` sur les numéros de suivi (`code_suivi`), emails, SIRET, etc.
4. **Valeurs par défaut** : Utiliser `DEFAULT CURRENT_TIMESTAMP` pour les horodatages d'enregistrement.
