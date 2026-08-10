-- =============================================================================
-- EXERCICE 4 : IDENTIFICATION ET OPTIMISATION DES TYPES DE COLONNES OVERSIZED
-- Objectif : Réduire la taille de la BDD en réduisant le nombre d'octets par ligne
-- =============================================================================

USE base_sirene;

-- 1. DÉTECTION DES COLONNES SURDIMENSIONNÉES VIA DES REQUÊTES D'INSPECTION
-- A. Trouver la longueur maximale réelle des valeurs dans des colonnes VARCHAR(255)
SELECT 
    MAX(CHAR_LENGTH(code_postal)) AS max_len_cp,        -- Longueur max réelle (ex: 5 -> CHAR(5))
    MAX(CHAR_LENGTH(code_departement)) AS max_len_dept, -- Longueur max réelle (ex: 3 -> VARCHAR(3))
    MAX(CHAR_LENGTH(code_activite)) AS max_len_ape      -- Longueur max réelle (ex: 6 -> VARCHAR(6))
FROM etablissements;

-- B. Vérifier si des colonnes BIGINT ou INT dépassent les limites de SMALLINT / MEDIUMINT
SELECT 
    MIN(effectif_entreprises) AS min_eff,
    MAX(effectif_entreprises) AS max_eff
FROM etablissements;

-- 2. APPLICATION DES MODIFICATIONS DE SCHÉMA (ALTER TABLE OPTIMISÉS)

-- A. Passer code_postal de VARCHAR(255) à CHAR(5) (Gain : 250 octets par ligne !)
ALTER TABLE etablissements MODIFY code_postal CHAR(5) NOT NULL;

-- B. Passer code_departement de VARCHAR(255) à VARCHAR(3)
ALTER TABLE etablissements MODIFY code_departement VARCHAR(3) NOT NULL;

-- C. Passer code_activite de VARCHAR(255) à VARCHAR(6)
ALTER TABLE etablissements MODIFY code_activite VARCHAR(6) NOT NULL;

-- D. Passer le statut_actif de INT à TINYINT(1) (Gain : 3 octets par ligne !)
ALTER TABLE etablissements MODIFY est_actif TINYINT(1) NOT NULL DEFAULT 1;

-- 3. REQUÊTE POUR AUDITER LA RÉDUCTION DE TAILLE SUR DISQUE
SELECT 
    table_name AS 'Table Optimisée',
    ROUND((data_length / 1024 / 1024), 2) AS 'Taille Données Après Optimisation (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'base_sirene';
