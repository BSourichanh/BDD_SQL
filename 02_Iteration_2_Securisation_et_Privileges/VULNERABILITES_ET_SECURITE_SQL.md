# 🛡️ Sécurisation & Vulnérabilités SQL — Mémo Complet (Itération 2)

> [!IMPORTANT] **Objectif Moodle (Itération 2)**
> Mettre en place les bonnes pratiques en matière de sécurité pour les applications (Java / PHP) connectées à une base de données SQL.
> **Livrables de l'itération** :
> 1. Mémo des failles de sécurité SQL rédigé.
> 2. Code d'accès aux données sécurisé (`PreparedStatement`).
> 3. Gestion rigoureuse des **Droits et Privilèges SQL** (`GRANT`, `REVOKE`, Principe du moindre privilège).
> 4. Base de données mise à jour / patchée et identifiants isolés (`.env`).

---

## 📑 Sommaire

- [1. Section 2.1 | Analyse des Vulnérabilités SQL](#1-section-21--analyse-des-vuln%C3%A9rabilit%C3%A9s-sql)
  - [1.1 | Injection SQL (SQL Injection - SQLi)](#11--injection-sql-sql-injection---sqli)
  - [1.2 | Stockage Sensible Non Sécurisé](#12--stockage-sensible-non-s%C3%A9curis%C3%A9)
  - [1.3 | Fuite des Identifiants BDD (*Hardcoded Credentials*)](#13--fuite-des-identifiants-bdd-hardcoded-credentials)
  - [1.4 | Sur-Privilège de l'Utilisateur SQL & Risques](#14--sur-privil%C3%A8ge-de-lutilisateur-sql--risques)
- [2. Section 2.2 | Correctifs & Implémentation Code](#2-section-22--correctifs--impl%C3%A9mentation-code)
  - [2.1 | Requêtes Préparées (`PreparedStatement`)](#21--requ%C3%AAtes-pr%C3%A9par%C3%A9es-preparedstatement)
  - [2.2 | Hashage des Mots de Passe (BCrypt / Argon2)](#22--hashage-des-mots-de-passe-bcrypt--argon2)
  - [2.3 | Gestion des Secrets via Fichier `.env`](#23--gestion-des-secrets-via-fichier-env)
- [3. Section 2.3 | Droits, Privilèges & Contrôle d'Accès SQL (Complet)](#3-section-23--droits-privil%C3%A8ges--contr%C3%B4le-dacc%C3%A8s-sql-complet)
  - [3.1 | Principe du Moindre Privilège (*PoLP*)](#31--principe-du-moindre-privil%C3%A8ge-polp)
  - [3.2 | Classification des Privilèges MySQL](#32--classification-des-privil%C3%A8ges-mysql)
  - [3.3 | Restriction des Hôtes de Connexion (`Host`)](#33--restriction-des-h%C3%B4tes-de-connexion-host)
  - [3.4 | Script d'Attribution & Révocation des Droits (`GRANT` / `REVOKE`)](#34--script-dattribution--r%C3%A9vocation-des-droits-grant--revoke)
  - [3.5 | Définition des Rôles Métier (Production, Reporting, Relais)](#35--d%C3%A9finition-des-r%C3%B4les-m%C3%A9tier-production-reporting-relais)
  - [3.6 | Audit et Inspection des Privilèges](#36--audit-et-inspection-des-privil%C3%A8ges)
- [4. Matrice de Test de Robustesse](#4-matrice-de-test-de-robustesse)
- [5. Checklist des Livrables Moodle](#5-checklist-des-livrables-moodle)

---

# 1. Section 2.1 | Analyse des Vulnérabilités SQL

## 1.1 | Injection SQL (SQL Injection - SQLi)

### 📌 Principe de la Faille
L'injection SQL survient lorsqu'une application construit une requête SQL dynamique en **concaténant directement** des chaînes de caractères saisies par l'utilisateur sans les nettoyer ni les paramétrer. L'attaquant peut ainsi injecter de la syntaxe SQL pour altérer la logique de la requête.

### 🔴 Exemple de Code Vulnérable en Java (JDBC)
```java
// ❌ DANGEREUX : Concaténation directe de la saisie utilisateur
String emailInput = request.getParameter("email");
String passwordInput = request.getParameter("password");

String query = "SELECT * FROM particuliers WHERE email = '" + emailInput + "' AND mot_de_passe = '" + passwordInput + "'";

Statement statement = connection.createStatement();
ResultSet resultSet = statement.executeQuery(query);
```

### 💣 Scénario d'Attaque 1 : Contournement d'Authentification (*Auth Bypass*)
- **Saisie de l'attaquant dans le champ password** : `' OR '1'='1`
- **Requête SQL exécutée par le serveur** :
  ```sql
  SELECT * FROM particuliers WHERE email = 'admin@email.fr' AND mot_de_passe = '' OR '1'='1';
  ```
- **Résultat** : La condition `'1'='1'` étant toujours vraie, la requête renvoie la première ligne sans connaître le mot de passe !

### 💣 Scénario d'Attaque 2 : Destruction / Altération de Données (*Stacked Queries*)
- **Saisie de l'attaquant dans un champ de recherche** : `COL-2026-001'; DROP TABLE colis; --`
- **Requête SQL exécutée** :
  ```sql
  SELECT * FROM colis WHERE code_suivi = 'COL-2026-001'; DROP TABLE colis; --';
  ```
- **Résultat** : La table `colis` est supprimée de la base de données !

---

## 1.2 | Stockage Sensible Non Sécurisé

### 📌 Principe de la Faille
Enregistrer des mots de passe en clair (texte brut) ou avec des fonctions de hachage obsolètes et rapides (MD5, SHA-1).

### ⚠️ Risque
Si un attaquant obtient une copie de la base de données (*database leak/dump*), il accède immédiatement à tous les mots de passe des utilisateurs en clair ou les déchiffre en quelques secondes via des tables arc-en-ciel (*rainbow tables*).

---

## 1.3 | Fuite des Identifiants BDD (*Hardcoded Credentials*)

### 📌 Principe de la Faille
Écrire les informations de connexion (`root`, mot de passe BDD, hôte) directement en dur dans le code source Java ou PHP.

---

## 1.4 | Sur-Privilège de l'Utilisateur SQL & Risques

### 📌 Principe de la Faille
Connecter l'application web avec le compte d'administration suprême (`root`).

### ⚠️ Risques Majeurs
- Si une injection SQL survient sous un compte `root`, l'attaquant dispose des droits de suppression de la base (`DROP DATABASE`), de modification du système de fichiers (`LOAD_FILE`, `SELECT INTO OUTFILE`) et d'arrêt du serveur MySQL (`SHUTDOWN`).

---

# 2. Section 2.2 | Correctifs & Implémentation Code

## 2.1 | Requêtes Préparées (`PreparedStatement`)

### 🛡️ Principe de Protection
Les **PreparedStatement** séparent le code SQL de la donnée. Le moteur de base de données compile d'abord la structure de la requête, puis insère les valeurs utilisateur comme de simples constantes textuelles. **Toute tentative d'injection SQL est ainsi neutralisée.**

### ✅ Code Java JDBC Sécurisé (Correctif)
```java
// ✅ SÉCURISÉ : Utilisation des jokers '?' avec PreparedStatement
String sql = "SELECT id_particulier, nom_particulier, email, statut_eligibilite " +
             "FROM particuliers WHERE email = ? AND mot_de_passe = ?";

try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
    pstmt.setString(1, emailInput);
    pstmt.setString(2, hashedPasswordInput);
    
    try (ResultSet rs = pstmt.executeQuery()) {
        if (rs.next()) {
            System.out.println("Connexion réussie pour : " + rs.getString("nom_particulier"));
        }
    }
}
```

### ✅ Code PHP PDO Sécurisé (Correctif)
```php
// ✅ SÉCURISÉ : Requête préparée avec paramètres nommés PDO
$sql = "SELECT * FROM colis WHERE code_suivi = :code AND id_transporteur = :transporteur";
$stmt = $pdo->prepare($sql);
$stmt->execute([
    ':code' => $codeSuiviInput,
    ':transporteur' => $transporteurIdInput
]);
$colis = $stmt->fetch(PDO::FETCH_ASSOC);
```

---

## 2.2 | Hashage des Mots de Passe (BCrypt / Argon2)

```java
import org.mindrot.jbcrypt.BCrypt;

public class SecurityService {
    public static String hashPassword(String rawPassword) {
        return BCrypt.hashpw(rawPassword, BCrypt.gensalt(12));
    }

    public static boolean verifyPassword(String rawPassword, String storedHash) {
        return BCrypt.checkpw(rawPassword, storedHash);
    }
}
```

---

## 2.3 | Gestion des Secrets via Fichier `.env`

```env
DB_CONNECTION=mysql
DB_HOST=172.17.0.1
DB_PORT=6603
DB_DATABASE=bdd_colis_relais
DB_USERNAME=app_colis_user
DB_PASSWORD=SecurePassword_2026!
```

---

# 3. Section 2.3 | Droits, Privilèges & Contrôle d'Accès SQL (Complet)

## 3.1 | Principe du Moindre Privilège (*PoLP*)

Le **Principe du Moindre Privilège** (*Principle of Least Privilege*) stipule qu'un utilisateur ou une application ne doit posséder **que les droits strictement nécessaires** à l'accomplissement de ses tâches, et rien de plus.

> [!CAUTION] **Règle d'or en Production**
> L'application Java/PHP ne doit **JAMAIS** posséder les droits DDL (`CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`) ni les droits d'administration (`GRANT`, `SUPER`, `SHUTDOWN`). Elle doit disposer uniquement des droits DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) sur sa propre base de données.

---

## 3.2 | Classification des Privilèges MySQL

MySQL / MariaDB découpe les privilèges en 3 grands niveaux :

| Catégorie | Privilèges | Rôle & Usage |
| :--- | :--- | :--- |
| **Administration (Globaux)** | `ALL PRIVILEGES`, `SUPER`, `CREATE USER`, `GRANT OPTION`, `SHUTDOWN`, `FILE` | Réservé à l'administrateur de base de données (DBA). |
| **Structure (DDL)** | `CREATE`, `ALTER`, `DROP`, `INDEX`, `CREATE VIEW` | Déploiement et migration de schéma. |
| **Données (DML)** | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | Exploitation courante par l'application web/mobile. |

---

## 3.3 | Restriction des Hôtes de Connexion (`Host`)

Le contrôle d'accès dans MySQL repose sur le couple `Utilisateur` + `Hôte` (`'utilisateur'@'hote'`) :

- `'app_user'@'localhost'` : Connexion autorisée **uniquement depuis la machine locale**.
- `'app_user'@'192.168.1.50'` : Connexion autorisée **uniquement depuis l'adresse IP du serveur d'application**.
- `'app_user'@'172.17.%.%'` : Connexion autorisée depuis le réseau interne des conteneurs Docker.
- ❌ `'app_user'@'%'` : À éviter en production sauf si filtré par un pare-feu (autorise n'importe quelle adresse IP).

---

## 3.4 | Script d'Attribution & Révocation des Droits (`GRANT` / `REVOKE`)

### A. Création d'un Utilisateur Applicatif Restreint
```sql
-- 1. Création de l'utilisateur restreint
CREATE USER 'app_colis_user'@'172.17.%.%' IDENTIFIED BY 'SecurePassword_2026!';

-- 2. Attribution explicite des droits DML uniquement sur la BDD bdd_colis_relais
GRANT SELECT, INSERT, UPDATE, DELETE ON bdd_colis_relais.* TO 'app_colis_user'@'172.17.%.%';

-- 3. Appliquer immédiatement les changements de droits
FLUSH PRIVILEGES;
```

### B. Révocation des Droits Dangereux (`REVOKE`)
Si des droits trop élevés avaient été accordés par erreur :
```sql
-- Révocation des droits de suppression de tables et d'altération de schéma
REVOKE DROP, ALTER, CREATE ON bdd_colis_relais.* FROM 'app_colis_user'@'172.17.%.%';

-- Appliquer les changements
FLUSH PRIVILEGES;
```

---

## 3.5 | Définition des Rôles Métier (Production, Reporting, Relais)

Pour une sécurité maximale, il est recommandé de créer des **rôles SQL spécifiques** selon l'usage :

```sql
USE bdd_colis_relais;

-- =============================================================================
-- RÔLE 1 : APPLICATION BACKEND (Production CRUD)
-- =============================================================================
CREATE ROLE IF NOT EXISTS 'role_app_backend';
GRANT SELECT, INSERT, UPDATE, DELETE ON bdd_colis_relais.* TO 'role_app_backend';

-- =============================================================================
-- RÔLE 2 : REPORTING / ANALYTICS (Lecture seule)
-- =============================================================================
CREATE ROLE IF NOT EXISTS 'role_reporting_readonly';
GRANT SELECT ON bdd_colis_relais.* TO 'role_reporting_readonly';

-- =============================================================================
-- RÔLE 3 : SERVICE POINT RELAIS (Accès restreint aux colis et statuts)
-- =============================================================================
CREATE ROLE IF NOT EXISTS 'role_point_relais';
GRANT SELECT ON bdd_colis_relais.colis TO 'role_point_relais';
GRANT UPDATE (statut_actuel, date_depot_relais, date_retrait) ON bdd_colis_relais.colis TO 'role_point_relais';
GRANT INSERT ON bdd_colis_relais.historique_statuts_colis TO 'role_point_relais';

-- =============================================================================
-- AFFECTATION DES RÔLES AUX UTILISATEURS APPLICATIFS
-- =============================================================================
CREATE USER IF NOT EXISTS 'user_web_api'@'%' IDENTIFIED BY 'WebPassword2026!';
CREATE USER IF NOT EXISTS 'user_bi_report'@'%' IDENTIFIED BY 'ReportPassword2026!';

GRANT 'role_app_backend' TO 'user_web_api'@'%';
GRANT 'role_reporting_readonly' TO 'user_bi_report'@'%';

SET DEFAULT ROLE ALL TO 'user_web_api'@'%', 'user_bi_report'@'%';
FLUSH PRIVILEGES;
```

---

## 3.6 | Audit et Inspection des Privilèges

Pour vérifier et auditer les droits accordés sur le serveur MySQL :

```sql
-- 1. Afficher les privilèges d'un utilisateur spécifique
SHOW GRANTS FOR 'app_colis_user'@'172.17.%.%';

-- 2. Inspecter tous les utilisateurs et leurs hôtes autorisés
SELECT User, Host, plugin, authentication_string FROM mysql.user;

-- 3. Lister les utilisateurs possédant le droit SUPER ou ALL PRIVILEGES
SELECT User, Host FROM mysql.user WHERE Super_priv = 'Y' OR Grant_priv = 'Y';
```

---

# 4. Matrice de Test de Robustesse

| Scénario de Test | Saisie Injectée | Résultat Avant Correctif | Résultat Après `PreparedStatement` & Privilèges Restreints |
| :--- | :--- | :--- | :--- |
| **Authentification** | `' OR '1'='1` | 🔴 **Faille** : Connexion réussie sans mot de passe | ✅ **Protégé** : Requête échoue (recherche exacte de la chaîne) |
| **Tentative DROP TABLE** | `COL-001'; DROP TABLE colis; --` | 🔴 **Faille** : Suppression de la table `colis` | ✅ **Protégé** : Erreur SQL `Access denied for user (no DROP privilege)` |
| **Saisie Caractères Spéciaux** | `<script>alert(1)</script>` | 🔴 **Faille** : Risque XSS / Erreur SQL | ✅ **Protégé** : Échappement et encodage correct |
| **Fuite de Base de Données** | *Lecture de la table particuliers* | 🔴 **Faille** : Mots de passe visibles en clair | ✅ **Protégé** : Hashs BCrypt inutilisables |

---

# 5. Checklist des Livrables Moodle

- [x] **Mémo des failles de sécurité SQL rédigé** (`VULNERABILITES_ET_SECURITE_SQL.md`)
- [x] **Code Java/PHP sécurisé** avec `PreparedStatement`
- [x] **Mots de passe hashés avec BCrypt**
- [x] **Gestion des droits & privilèges SQL configurée** (`GRANT`, `REVOKE`, Rôles SQL)
- [x] **Fichier de secrets `.env` mis en place** et ajouté au `.gitignore`
- [x] **Script de Patch BDD et utilisateur restreint appliqué** (`07_patch_securite.sql`)
