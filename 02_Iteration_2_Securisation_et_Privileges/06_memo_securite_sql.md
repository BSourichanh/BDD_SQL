# 🛡️ 06 — Mémo de Sécurité SQL & Bonnes Pratiques Code (Itération 2)

> [!IMPORTANT]
> Ce mémo détaille les vulnérabilités courantes lors de l'interaction entre une application (Java / PHP) et une base de données SQL, ainsi que les mesures de protection indispensables à mettre en œuvre.

---

## 1. Analyse des Vulnérabilités SQL

### A. Injection SQL (SQL Injection - SQLi)
- **Principe** : L'attaquant injecte du code SQL arbitraire dans les champs de saisie (formulaire, paramètres d'URL, headers) pour modifier la logique de la requête exécutée par le serveur.
- **Exemple de code vulnérable (Java)** :
  ```java
  // ❌ TRÈS DANGEREUX : Concaténation directe de variables utilisateur
  String query = "SELECT * FROM particuliers WHERE email = '" + inputEmail + "' AND mot_de_passe = '" + inputPassword + "'";
  Statement stmt = connection.createStatement();
  ResultSet rs = stmt.executeQuery(query);
  ```
  *Si l'utilisateur saisit `' OR '1'='1` comme mot de passe, la clause WHERE devient toujours vraie (`TRUE`), contournant l'authentification.*

### B. Stockage de Données Sensibles en Texte Brut
- **Danger** : Conserver des mots de passe ou numéros confidentiels non chiffrés / non hashés en BDD. En cas de fuite de la base de données (dump, sauvegarde exposée), les comptes sont directement compromis.

### C. Identifiants BDD Codés en Dur (*Hardcoded Credentials*)
- **Danger** : Écrire l'utilisateur `root` et le mot de passe BDD directement dans le code source Java ou PHP. Ces accès finissent exposés sur les dépôts Git.

---

## 2. Solutions & Pratiques de Sécurisation

### A. Utilisation Obligatoire de Requêtes Préparées (`PreparedStatement`)

Les requêtes préparées séparent le code SQL des données. Le serveur de BDD compile la structure de la requête à l'avance et traite les entrées utilisateur uniquement comme des constantes (littéraux), annulant toute tentative d'injection.

#### Exemple en Java (Correct ✅) :
```java
// ✅ SÉCURISÉ : Requête paramétrée avec PreparedStatement
String sql = "SELECT id_particulier, nom_particulier, email, statut_eligibilite " +
             "FROM particuliers WHERE email = ? AND statut_eligibilite = ?";

try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
    pstmt.setString(1, inputEmail);
    pstmt.setString(2, "ACTIF");
    
    try (ResultSet rs = pstmt.executeQuery()) {
        if (rs.next()) {
            System.out.println("Particulier trouvé : " + rs.getString("nom_particulier"));
        }
    }
}
```

#### Exemple en PHP PDO (Correct ✅) :
```php
// ✅ SÉCURISÉ : Requête paramétrée avec PDO
$sql = "SELECT * FROM colis WHERE code_suivi = :code_suivi";
$stmt = $pdo->prepare($sql);
$stmt->execute([':code_suivi' => $codeSuiviInput]);
$colis = $stmt->fetch();
```

---

### B. Hashage Sécurisé des Mots de Passe

- Utiliser un algorithme de hashage robuste et lent avec salage automatique : **BCrypt**, **Argon2id**, ou **PBKDF2**.
- Ne jamais utiliser MD5, SHA-1 ou SHA-256 direct (trop rapides et vulnérables aux tables arc-en-ciel).

```java
// Exemple d'utilisation de BCrypt en Java
String hashedPassword = BCrypt.hashpw(rawPassword, BCrypt.gensalt(12));

// Vérification lors de la connexion
if (BCrypt.checkpw(inputPassword, storedHash)) {
    // Connexion autorisée
}
```

---

### C. Isolation des Paramètres d'Accès BDD

- Placer les identifiants dans un fichier `.env` ou dans des variables d'environnement hors du contrôle de version (ajouter `.env` dans `.gitignore`).

```env
DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=6603
DB_DATABASE=bdd_colis_relais
DB_USERNAME=app_user
DB_PASSWORD=MotDePasseComplexe!2026
```

---

### D. Principe du Moindre Privilège SQL

Ne pas utiliser le compte `root` MySQL dans l'application. Créer un utilisateur applicatif dédié avec uniquement les privilèges requis :

```sql
-- Création d'un utilisateur applicatif restreint
CREATE USER 'app_colis'@'%' IDENTIFIED BY 'MotDePasseComplexe!2026';
GRANT SELECT, INSERT, UPDATE ON bdd_colis_relais.* TO 'app_colis'@'%';
FLUSH PRIVILEGES;
```
