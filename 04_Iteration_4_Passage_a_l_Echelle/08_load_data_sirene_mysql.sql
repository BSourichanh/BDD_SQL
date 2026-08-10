-- =============================================================================
-- SCRIPT D'IMPORTATION NATIVE MYSQL (LOAD DATA INFILE) DES CSV SIRENE
-- Exercice 1 : Créer la base avec les unités légales et établissements actifs
-- =============================================================================

-- Désactivation temporaire du mode SQL strict pour tolérer les champs dates vides ("")
SET GLOBAL sql_mode = '';
SET SESSION sql_mode = '';
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS base_sirene
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE base_sirene;

-- 1. STAGING TABLE / CREATION DES TABLES UNITES LEGALES ET ETABLISSEMENTS
CREATE TABLE IF NOT EXISTS unites_legales (
    siren VARCHAR(9) PRIMARY KEY,
    statut_diffusion VARCHAR(5),
    unite_purgee VARCHAR(10),
    date_creation DATE NULL,
    sigle VARCHAR(20),
    sexe VARCHAR(5),
    prenom1 VARCHAR(50),
    prenom2 VARCHAR(50),
    prenom3 VARCHAR(50),
    prenom4 VARCHAR(50),
    prenom_usuel VARCHAR(50),
    pseudonyme VARCHAR(50),
    identifiant_association VARCHAR(50),
    tranche_effectifs VARCHAR(10),
    annee_effectifs VARCHAR(10),
    date_dernier_traitement DATETIME NULL,
    nombre_periodes INT NULL,
    categorie_entreprise VARCHAR(10),
    annee_categorie_entreprise VARCHAR(10),
    date_debut DATE NULL,
    etat_administratif CHAR(1),
    nom VARCHAR(100),
    nom_usage VARCHAR(100),
    denomination VARCHAR(150),
    denomination_usuelle1 VARCHAR(150),
    denomination_usuelle2 VARCHAR(150),
    denomination_usuelle3 VARCHAR(150),
    categorie_juridique VARCHAR(10),
    code_activite VARCHAR(10),
    nomenclature_activite VARCHAR(20),
    nic_siege VARCHAR(10),
    economie_sociale_solidaire VARCHAR(5),
    societe_mission VARCHAR(5),
    caractere_employeur VARCHAR(5),
    activite_principale_naf VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS etablissements (
    siret VARCHAR(14) PRIMARY KEY,
    siren VARCHAR(9) NOT NULL,
    nic VARCHAR(5),
    statut_diffusion VARCHAR(5),
    date_creation DATE NULL,
    tranche_effectifs VARCHAR(10),
    annee_effectifs VARCHAR(10),
    activite_principale_registre VARCHAR(10),
    date_dernier_traitement DATETIME NULL,
    etablissement_siege VARCHAR(10),
    nombre_periodes INT NULL,
    code_postal CHAR(5),
    code_departement VARCHAR(3),
    code_activite VARCHAR(10),
    etat_administratif CHAR(1) NOT NULL DEFAULT 'A',
    est_actif TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- 2. IMPORTATION NATIVE PAR LOAD DATA INFILE (MySQL / MariaDB)

-- Import Unités Légales (IGNORE les doublons de clés primaires)
LOAD DATA INFILE '/var/lib/mysql-files/StockUniteLegale_utf8.csv'
IGNORE INTO TABLE unites_legales
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- Import Établissements (IGNORE les doublons de SIRET)
LOAD DATA INFILE '/var/lib/mysql-files/StockEtablissement_utf8.csv'
IGNORE INTO TABLE etablissements
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- 3. FILTRER UNIQUEMENT LES UNITÉS ET ÉTABLISSEMENTS ACTIFS (Exigence Moodle)
DELETE FROM etablissements WHERE etat_administratif <> 'A';
DELETE FROM unites_legales WHERE etat_administratif <> 'A';
