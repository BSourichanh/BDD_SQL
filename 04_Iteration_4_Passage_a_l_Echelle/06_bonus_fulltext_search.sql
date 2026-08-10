-- =============================================================================
-- EXERCICE BONUS : RECHERCHE TEXTUELLE & INDEXATION FULLTEXT
-- Benchmark : SELECT ... LIKE '%term%' VS MATCH(...) AGAINST(...)
-- =============================================================================

USE base_sirene;

-- 1. MESURER LA TAILLE AVANT INDEXATION FULLTEXT
SELECT 
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Taille Initiale (MB)'
FROM information_schema.TABLES
WHERE table_name = 'unites_legales' AND table_schema = 'base_sirene';

-- 2. BENCHMARK TEMPS D'EXÉCUTION AVEC RECHERCHE CLASSIQUE (LIKE)
-- Note : Un LIKE avec wildcard au début (%boulangerie%) provoque un Full Table Scan !
EXPLAIN ANALYZE 
SELECT siren, denomination 
FROM unites_legales 
WHERE denomination LIKE '%Boulangerie%';

-- 3. CONFIGURER L'INDEX FULLTEXT SUR LA DÉNOMINATION
ALTER TABLE unites_legales ADD FULLTEXT INDEX ft_idx_denomination(denomination);

-- 4. MESURER LA NOUVELLE TAILLE DE LA BASE ET DE L'INDEX FULLTEXT
SELECT 
    ROUND((index_length / 1024 / 1024), 2) AS 'Taille Index FULLTEXT (MB)'
FROM information_schema.TABLES
WHERE table_name = 'unites_legales' AND table_schema = 'base_sirene';

-- 5. BENCHMARK TEMPS D'EXÉCUTION AVEC RECHERCHE MATCH(...) AGAINST(...)
EXPLAIN ANALYZE 
SELECT siren, denomination 
FROM unites_legales 
WHERE MATCH(denomination) AGAINST('+Boulangerie' IN BOOLEAN MODE);
