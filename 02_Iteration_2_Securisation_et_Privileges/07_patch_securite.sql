-- =============================================================================
-- SCRIPT DE PATCH SÉCURITÉ, DROITS & PRIVILÈGES SQL (Itération 2)
-- Projet : Gestion de Livraison de Colis en Points Relais à Domicile
-- =============================================================================

USE bdd_colis_relais;

-- 1. PATCH BDD : Ajouter la colonne mot_de_passe hashé dans la table particuliers
ALTER TABLE particuliers 
ADD COLUMN IF NOT EXISTS mot_de_passe VARCHAR(255) NOT NULL DEFAULT '$2a$12$ExampleHashForBCryptPasswordStoragePlaceholderXX';

-- 2. PATCH BDD : Ajouter la colonne mot_de_passe hashé dans la table clients
ALTER TABLE clients 
ADD COLUMN IF NOT EXISTS mot_de_passe VARCHAR(255) NOT NULL DEFAULT '$2a$12$ExampleHashForBCryptPasswordStoragePlaceholderXX';

-- 3. GESTION DES RÔLES SQL (Principe du moindre privilège)
-- Rôle 1 : Application Backend (Production CRUD)
CREATE ROLE IF NOT EXISTS 'role_app_backend';
GRANT SELECT, INSERT, UPDATE, DELETE ON bdd_colis_relais.* TO 'role_app_backend';

-- Rôle 2 : Reporting & Analytics (Lecture seule)
CREATE ROLE IF NOT EXISTS 'role_reporting_readonly';
GRANT SELECT ON bdd_colis_relais.* TO 'role_reporting_readonly';

-- 4. CRÉATION DES UTILISATEURS APPLICATIFS RESTREINTS
DROP USER IF EXISTS 'app_colis_user'@'%';
DROP USER IF EXISTS 'app_colis_user'@'172.17.%.%';
DROP USER IF EXISTS 'user_bi_report'@'%';

-- Utilisateur Backend Production (Réseau Docker/Local)
CREATE USER 'app_colis_user'@'%' IDENTIFIED BY 'SecurePassword_2026!';
GRANT 'role_app_backend' TO 'app_colis_user'@'%';
SET DEFAULT ROLE 'role_app_backend' TO 'app_colis_user'@'%';

-- Utilisateur Reporting (Lecture seule)
CREATE USER 'user_bi_report'@'%' IDENTIFIED BY 'ReportPassword2026!';
GRANT 'role_reporting_readonly' TO 'user_bi_report'@'%';
SET DEFAULT ROLE 'role_reporting_readonly' TO 'user_bi_report'@'%';

-- 5. ACTUALISATION ET VÉRIFICATION DES PRIVILÈGES
FLUSH PRIVILEGES;

-- Affichage des privilèges accordés pour l'audit
SHOW GRANTS FOR 'app_colis_user'@'%';
