-- =============================================================================
-- SCRIPT DE CRÉATION DE LA BASE DE DONNÉES : bdd_colis_relais (DDL Optimisé)
-- Projet : Gestion de Livraison de Colis en Points Relais à Domicile
-- Version : 1.1 (Itération 1 - Harmonisé & Optimisé)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS bdd_colis_relais
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE bdd_colis_relais;

-- Supprimer les tables dans l'ordre inverse des dépendances si elles existent déjà
DROP TABLE IF EXISTS historique_statuts_colis;
DROP TABLE IF EXISTS colis;
DROP TABLE IF EXISTS missions;
DROP TABLE IF EXISTS particuliers;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS transporteurs;

-- =============================================================================
-- NIVEAU 0 : Tables sans clés étrangères
-- =============================================================================

-- 1. Table TRANSPORTEURS (Entreprises partenaires logistiques)
CREATE TABLE transporteurs (
    id_transporteur INT AUTO_INCREMENT PRIMARY KEY,
    nom_societe VARCHAR(100) NOT NULL UNIQUE,
    siret VARCHAR(14) NOT NULL UNIQUE,
    email_contact VARCHAR(100) NOT NULL,
    telephone_contact VARCHAR(20) NOT NULL,
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    date_partenariat DATE NOT NULL,
    CONSTRAINT chk_siret_length CHECK (CHAR_LENGTH(siret) = 14)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Table CLIENTS (Destinataires finaux des colis)
CREATE TABLE clients (
    id_client INT AUTO_INCREMENT PRIMARY KEY,
    nom_client VARCHAR(50) NOT NULL,
    prenom_client VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telephone VARCHAR(20) NOT NULL,
    adresse_rue VARCHAR(255) NOT NULL,
    code_postal VARCHAR(10) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    date_inscription DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Table PARTICULIERS (Points Relais à domicile)
CREATE TABLE particuliers (
    id_particulier INT AUTO_INCREMENT PRIMARY KEY,
    nom_particulier VARCHAR(50) NOT NULL,
    prenom_particulier VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telephone VARCHAR(20) NOT NULL,
    adresse_rue VARCHAR(255) NOT NULL,
    adresse_complement VARCHAR(100) DEFAULT NULL,
    code_postal VARCHAR(10) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    type_logement ENUM('Maison', 'Appartement') NOT NULL,
    capacite_stockage_colis INT NOT NULL DEFAULT 5,
    disponibilites_description TEXT DEFAULT NULL,
    statut_eligibilite ENUM('EN_ATTENTE', 'ACTIF', 'INACTIF', 'SUSPENDU') NOT NULL DEFAULT 'EN_ATTENTE',
    date_inscription DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_capacite_positive CHECK (capacite_stockage_colis > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- NIVEAU 1 : Tables dépendant des tables de Niveau 0
-- =============================================================================

-- 4. Table MISSIONS (Partenariat temporaire entre Point Relais et Transporteur)
CREATE TABLE missions (
    id_mission INT AUTO_INCREMENT PRIMARY KEY,
    id_particulier INT NOT NULL,
    id_transporteur INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE DEFAULT NULL,
    statut_mission ENUM('EN_COURS', 'TERMINEE', 'SUSPENDUE') NOT NULL DEFAULT 'EN_COURS',
    CONSTRAINT fk_missions_particulier FOREIGN KEY (id_particulier) 
        REFERENCES particuliers(id_particulier) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_missions_transporteur FOREIGN KEY (id_transporteur) 
        REFERENCES transporteurs(id_transporteur) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_dates_mission CHECK (date_fin IS NULL OR date_fin >= date_debut)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- NIVEAU 2 : Table COLIS (Élément central du système)
-- =============================================================================

-- 5. Table COLIS
CREATE TABLE colis (
    id_colis INT AUTO_INCREMENT PRIMARY KEY,
    code_suivi VARCHAR(50) NOT NULL UNIQUE,
    poids_kg DECIMAL(5,2) NOT NULL,
    longueur_cm INT DEFAULT NULL,
    largeur_cm INT DEFAULT NULL,
    hauteur_cm INT DEFAULT NULL,
    est_fragile BOOLEAN NOT NULL DEFAULT FALSE,
    id_transporteur INT NOT NULL,
    id_client INT NOT NULL,
    id_point_relais INT DEFAULT NULL,
    statut_actuel ENUM(
        'EN_COURS_LIVRAISON', 
        'AU_POINT_RELAIS', 
        'RETIRE', 
        'NON_RECLAME', 
        'EN_RETOUR_TRANSPORTEUR', 
        'LIVRAISON_TERMINEE'
    ) NOT NULL DEFAULT 'EN_COURS_LIVRAISON',
    date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_depot_relais DATETIME DEFAULT NULL,
    date_limite_retrait DATETIME DEFAULT NULL,
    date_retrait DATETIME DEFAULT NULL,
    CONSTRAINT fk_colis_transporteur FOREIGN KEY (id_transporteur) 
        REFERENCES transporteurs(id_transporteur) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_colis_client FOREIGN KEY (id_client) 
        REFERENCES clients(id_client) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_colis_point_relais FOREIGN KEY (id_point_relais) 
        REFERENCES particuliers(id_particulier) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_poids_positif CHECK (poids_kg > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- NIVEAU 3 : Traçabilité et Historique
-- =============================================================================

-- 6. Table HISTORIQUE_STATUTS_COLIS
CREATE TABLE historique_statuts_colis (
    id_historique INT AUTO_INCREMENT PRIMARY KEY,
    id_colis INT NOT NULL,
    statut ENUM(
        'EN_COURS_LIVRAISON', 
        'AU_POINT_RELAIS', 
        'RETIRE', 
        'NON_RECLAME', 
        'EN_RETOUR_TRANSPORTEUR', 
        'LIVRAISON_TERMINEE'
    ) NOT NULL,
    date_changement DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_point_relais INT DEFAULT NULL,
    id_transporteur INT DEFAULT NULL,
    commentaire VARCHAR(255) DEFAULT NULL,
    CONSTRAINT fk_historique_colis FOREIGN KEY (id_colis) 
        REFERENCES colis(id_colis) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_historique_point_relais FOREIGN KEY (id_point_relais) 
        REFERENCES particuliers(id_particulier) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_historique_transporteur FOREIGN KEY (id_transporteur) 
        REFERENCES transporteurs(id_transporteur) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- INDEX POUR L'OPTIMISATION DES REQUÊTES FRÉQUENTES
-- =============================================================================
CREATE INDEX idx_colis_statut ON colis(statut_actuel);
CREATE INDEX idx_colis_point_relais ON colis(id_point_relais);
CREATE INDEX idx_colis_code_suivi ON colis(code_suivi);
CREATE INDEX idx_particuliers_ville ON particuliers(ville, code_postal);
CREATE INDEX idx_historique_colis_date ON historique_statuts_colis(id_colis, date_changement);
