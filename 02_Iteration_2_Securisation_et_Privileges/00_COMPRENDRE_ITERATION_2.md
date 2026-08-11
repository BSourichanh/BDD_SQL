# 🎓 Guide de Compréhension — Itération 2 : Sécurisation & Privilèges SQL

Ce document résume **tout ce qu'il faut comprendre et maîtriser** pour l'Itération 2 (Sécurité des bases de données SQL).

---

## 📍 Étape 1 : Les Injections SQL (La Faille N°1)
- **Ce qu'il faut comprendre** : Une injection SQL se produit lorsque le code concatène directement des données saisies par l'utilisateur dans la requête SQL :
  ```sql
  -- DANGEREUX : Concaténation brute
  "SELECT * FROM users WHERE user = '" + input + "' AND pass = '" + password + "'";
  ```
  Si l'attaquant saisit `' OR '1'='1`, la condition devient toujours vraie et la sécurité est contournée.

---

## 📍 Étape 2 : La Solution — Les Requêtes Préparées (PreparedStatement)
- **Ce qu'il faut comprendre** : Les **requêtes préparées** séparent la structure SQL des données saisies :
  ```java
  // SÉCURISÉ : Requête préparée
  PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE user = ? AND pass = ?");
  pstmt.setString(1, userInput);
  ```
  Le moteur SQL traite les paramètres uniquement comme des valeurs textuelles, annulant toute tentative d'injection.

---

## 📍 Étape 3 : Stockage Sécurisé des Mots de Passe (Hachage)
- **Ce qu'il faut comprendre** : **Jamais de mots de passe en texte brut en BDD !**
  - Utilisation d'un algorithme de hachage à sens unique robuste avec **Sel (Salt)** : **BCrypt** ou **Argon2**.
  - La BDD stocke le hash `$2a$12$...`. Lors de la connexion, on vérifie `BCrypt.checkpw(password, hash)`.

---

## 📍 Étape 4 : Gestion des Utilisateurs et Privilèges SQL
- **Ce qu'il faut comprendre** : Appliquer le principe du **moindre privilège**. L'application web ne doit jamais se connecter en `root` !
  - **Création d'un utilisateur dédié** :
    ```sql
    CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'MotDePasseSecurise123!';
    ```
  - **Attribution des droits stricts (GRANT)** :
    ```sql
    GRANT SELECT, INSERT, UPDATE ON bdd_colis.* TO 'app_user'@'localhost';
    FLUSH PRIVILEGES;
    ```
  - **Révocation des droits dangereux (REVOKE)** :
    ```sql
    REVOKE DROP, ALTER, DELETE ON bdd_colis.* FROM 'app_user'@'localhost';
    ```
