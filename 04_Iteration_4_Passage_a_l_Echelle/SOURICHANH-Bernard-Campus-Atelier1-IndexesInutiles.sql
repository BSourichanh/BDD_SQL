-- =============================================================================
-- EXERCICE 3 : IDENTIFICATION ET SUPPRESSION DES INDEX INUTILES / REDONDANTS
-- Objectif : Réduire l'empreinte RAM et disque de la base de données volumineuse
-- =============================================================================

USE base_sirene;

-- 1. REQUÊTE POUR AUDITER LA TAILLE DE LA BASE ET DE SES INDEX
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Taille Totale (MB)',
    ROUND((data_length / 1024 / 1024), 2) AS 'Données (MB)',
    ROUND((index_length / 1024 / 1024), 2) AS 'Index (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'base_sirene';

-- 2. DÉTECTION DES INDEX NON UTILISÉS / REDONDANTS (Statistiques Performance Schema)
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
  AND count_star = 0
  AND object_schema = 'base_sirene'
ORDER BY object_name, index_name;

-- 3. EXEMPLES DE SUPPRESSION D'INDEX REDONDANTS
-- Supprimer un index simple sur (code_postal) s'il existe déjà un index composite sur (code_postal, code_activite)
DROP INDEX idx_etablissements_cp_simple ON etablissements;

-- Supprimer les index sur des colonnes à très faible cardinalité (ex: booléens, statuts)
DROP INDEX idx_etablissements_est_actif ON etablissements;

-- 4. VÉRIFICATION DE LA GAIN DE TAILLE APRÈS SUPPRESSION
SELECT 
    ROUND(SUM(index_length / 1024 / 1024), 2) AS 'Taille Totale Index Après Nettoyage (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'base_sirene';
