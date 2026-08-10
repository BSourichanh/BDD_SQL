# 📖 02 — Dictionnaire de Données (Optimisé & Harmonisé)

> [!NOTE]
> Le dictionnaire de données répertorie l'ensemble des éléments d'information du système de gestion des colis et points relais.
> **Optimisation apportée** : Harmonisation stricte des types SQL avec le script DDL (`ENUM` vs `VARCHAR`), clarification des règles de gestion, précision des clés primaires (PK) / étrangères (FK) et explications des contraintes métier (ex: règle des 14 jours).

---

## 🛠️ Synthèse des Optimisations Apportées

1. **Typage SQL Explicite** : Remplacement des types génériques `VARCHAR` par des types `ENUM(...)` stricts pour garantir la cohérence des statuts au niveau du SGBD.
2. **Clés & Intégrité Référentielle** : Explicitation des clés étrangères (FK) et de la table parente référencée pour chaque relation.
3. **Règles de Gestion Embarquées** : Ajout des règles métier (ex: calcul automatique de la date limite de retrait `date_depot_relais + 14 jours`, vérification de la taille SIRET à 14 caractères).
4. **Attribut de Traçabilité Colis (`date_retrait`)** : Ajout explicite du champ `date_retrait` dans la table `colis` pour enregistrer l'horodatage exact du retrait par le client ou de la récupération par le transporteur sans nécessiter de sous-requête complexe sur l'historique.

---

## 1. Table `particuliers` (Points Relais à Domicile)

| Code Mnémonique | Désignation / Description | Type SQL | Taille / Format | Obligatoire | Clé | Contraintes & Règle de Gestion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_particulier` | Identifiant unique du particulier | `INT` | Auto-increment | **Oui** | **PK** | Clé primaire auto-générée |
| `nom_particulier` | Nom de famille | `VARCHAR` | 50 | **Oui** | - | Nom du particulier relais |
| `prenom_particulier` | Prénom | `VARCHAR` | 50 | **Oui** | - | Prénom du particulier relais |
| `email` | Adresse de courrier électronique | `VARCHAR` | 100 | **Oui** | - | `UNIQUE`, identifiant de connexion |
| `telephone` | Numéro de téléphone mobile | `VARCHAR` | 20 | **Oui** | - | Notification SMS / Contact |
| `adresse_rue` | Adresse du logement (rue et numéro) | `VARCHAR` | 255 | **Oui** | - | Emplacement du point relais |
| `adresse_complement` | Complément d'adresse (bâtiment, étage) | `VARCHAR` | 100 | Non | - | Facultatif (`NULL` par défaut) |
| `code_postal` | Code postal | `VARCHAR` | 10 | **Oui** | - | Ex: `75011`, `34000` |
| `ville` | Ville de résidence | `VARCHAR` | 100 | **Oui** | - | Filtrage géographique des relais |
| `type_logement` | Type de logement | `ENUM` | 'Maison', 'Appartement' | **Oui** | - | Éligibilité au stockage |
| `capacite_stockage_colis`| Nombre max de colis simultanés | `INT` | - | **Oui** | - | `DEFAULT 5`, `CHECK (capacite > 0)` |
| `disponibilites_description`| Descriptif des plages horaires | `TEXT` | - | Non | - | Horaires d'ouverture au retrait |
| `statut_eligibilite` | État d'activation du point relais | `ENUM` | 'EN_ATTENTE', 'ACTIF', 'INACTIF', 'SUSPENDU' | **Oui** | - | Validation par transporteur/admin |
| `date_inscription` | Date de création du compte | `DATETIME` | - | **Oui** | - | `DEFAULT CURRENT_TIMESTAMP` |

---

## 2. Table `transporteurs` (Entreprises Logistiques Partenaires)

| Code Mnémonique | Désignation / Description | Type SQL | Taille / Format | Obligatoire | Clé | Contraintes & Règle de Gestion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_transporteur` | Identifiant unique du transporteur | `INT` | Auto-increment | **Oui** | **PK** | Clé primaire |
| `nom_societe` | Raison sociale de l'entreprise | `VARCHAR` | 100 | **Oui** | - | `UNIQUE` (ex: DHL, Chronopost) |
| `siret` | Numéro SIRET légal | `VARCHAR` | 14 | **Oui** | - | `UNIQUE`, `CHECK (CHAR_LENGTH = 14)` |
| `email_contact` | Email du service logistique | `VARCHAR` | 100 | **Oui** | - | Contact professionnel |
| `telephone_contact` | Téléphone du contact professionnel | `VARCHAR` | 20 | **Oui** | - | Support transporteur |
| `est_actif` | Statut du partenariat | `BOOLEAN` | - | **Oui** | - | `DEFAULT TRUE` |
| `date_partenariat` | Date de signature du partenariat | `DATE` | - | **Oui** | - | Date d'entrée dans le réseau |

---

## 3. Table `missions` (Affectation Point Relais <-> Transporteur)

| Code Mnémonique | Désignation / Description | Type SQL | Taille / Format | Obligatoire | Clé | Contraintes & Règle de Gestion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_mission` | Identifiant unique de la mission | `INT` | Auto-increment | **Oui** | **PK** | Clé primaire |
| `id_particulier` | Particulier effectuant la mission | `INT` | - | **Oui** | **FK** | Référence `particuliers(id_particulier)` |
| `id_transporteur` | Transporteur partenaire ordonnateur | `INT` | - | **Oui** | **FK** | Référence `transporteurs(id_transporteur)` |
| `date_debut` | Date de début de la mission | `DATE` | - | **Oui** | - | Début de l'habilitation relais |
| `date_fin` | Date de fin prévue de la mission | `DATE` | - | Non | - | `CHECK (date_fin IS NULL OR date_fin >= date_debut)` |
| `statut_mission` | État d'activité de la mission | `ENUM` | 'EN_COURS', 'TERMINEE', 'SUSPENDUE' | **Oui** | - | `DEFAULT 'EN_COURS'` |

---

## 4. Table `clients` (Destinataires Finaux des Colis)

| Code Mnémonique | Désignation / Description | Type SQL | Taille / Format | Obligatoire | Clé | Contraintes & Règle de Gestion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_client` | Identifiant unique du client final | `INT` | Auto-increment | **Oui** | **PK** | Clé primaire |
| `nom_client` | Nom de famille | `VARCHAR` | 50 | **Oui** | - | Identité du destinataire |
| `prenom_client` | Prénom | `VARCHAR` | 50 | **Oui** | - | Identité du destinataire |
| `email` | Adresse email du client | `VARCHAR` | 100 | **Oui** | - | `UNIQUE`, notification de livraison |
| `telephone` | Téléphone mobile | `VARCHAR` | 20 | **Oui** | - | Alerte SMS d'arrivée de colis |
| `adresse_rue` | Adresse résidentielle | `VARCHAR` | 255 | **Oui** | - | Adresse du client |
| `code_postal` | Code postal | `VARCHAR` | 10 | **Oui** | - | Zone géographique client |
| `ville` | Ville | `VARCHAR` | 100 | **Oui** | - | Ville du client |
| `date_inscription` | Date de création de la fiche | `DATETIME` | - | **Oui** | - | `DEFAULT CURRENT_TIMESTAMP` |

---

## 5. Table `colis` (Élément Central du Système)

| Code Mnémonique | Désignation / Description | Type SQL | Taille / Format | Obligatoire | Clé | Contraintes & Règle de Gestion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_colis` | Identifiant technique interne | `INT` | Auto-increment | **Oui** | **PK** | Clé primaire |
| `code_suivi` | Numéro de suivi unique | `VARCHAR` | 50 | **Oui** | - | `UNIQUE` (ex: `COL-2026-001`) |
| `poids_kg` | Poids du colis en kilogrammes | `DECIMAL` | (5,2) | **Oui** | - | `CHECK (poids_kg > 0)` |
| `longueur_cm` | Longueur en cm | `INT` | - | Non | - | Dimensions physiques facultatives |
| `largeur_cm` | Largeur en cm | `INT` | - | Non | - | Dimensions physiques facultatives |
| `hauteur_cm` | Hauteur en cm | `INT` | - | Non | - | Dimensions physiques facultatives |
| `est_fragile` | Indicateur de fragilité | `BOOLEAN` | - | **Oui** | - | `DEFAULT FALSE` |
| `id_transporteur` | Transporteur responsable | `INT` | - | **Oui** | **FK** | Référence `transporteurs(id_transporteur)` |
| `id_client` | Client destinataire | `INT` | - | **Oui** | **FK** | Référence `clients(id_client)` |
| `id_point_relais` | Point relais actuel | `INT` | - | Non | **FK** | Référence `particuliers(id_particulier)`, `NULL` si en transit |
| `statut_actuel` | État courant du colis | `ENUM` | 'EN_COURS_LIVRAISON', 'AU_POINT_RELAIS', 'RETIRE', 'NON_RECLAME', 'EN_RETOUR_TRANSPORTEUR', 'LIVRAISON_TERMINEE' | **Oui** | - | `DEFAULT 'EN_COURS_LIVRAISON'` |
| `date_creation` | Date d'enregistrement | `DATETIME` | - | **Oui** | - | `DEFAULT CURRENT_TIMESTAMP` |
| `date_depot_relais` | Date de dépôt physique chez le relais | `DATETIME` | - | Non | - | Renseigné lors du dépôt au point relais |
| `date_limite_retrait`| Date limite de retrait client | `DATETIME` | - | Non | - | Règle des 14j : `date_depot_relais + 14 jours` |
| `date_retrait` | Date de retrait/récupération effectif | `DATETIME` | - | Non | - | Renseigné lors du retrait par le client ou transporteur |

---

## 6. Table `historique_statuts_colis` (Journalisation & Traçabilité)

| Code Mnémonique | Désignation / Description | Type SQL | Taille / Format | Obligatoire | Clé | Contraintes & Règle de Gestion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_historique` | Identifiant unique du journal | `INT` | Auto-increment | **Oui** | **PK** | Clé primaire |
| `id_colis` | Colis tracé | `INT` | - | **Oui** | **FK** | Référence `colis(id_colis) ON DELETE CASCADE` |
| `statut` | Statut à cet instant | `ENUM` | Mêmes valeurs que `statut_actuel` | **Oui** | - | Statut atteint lors de l'événement |
| `date_changement` | Date et heure de l'événement | `DATETIME` | - | **Oui** | - | `DEFAULT CURRENT_TIMESTAMP` |
| `id_point_relais` | Point relais associé à l'événement | `INT` | - | Non | **FK** | Référence `particuliers(id_particulier)` |
| `id_transporteur` | Transporteur associé à l'événement | `INT` | - | Non | **FK** | Référence `transporteurs(id_transporteur)` |
| `commentaire` | Motif ou remarque d'exploitation | `VARCHAR` | 255 | Non | - | Ex: `Remis au client`, `Non réclamé > 14j` |
