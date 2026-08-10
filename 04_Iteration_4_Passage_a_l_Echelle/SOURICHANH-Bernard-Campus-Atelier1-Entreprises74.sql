-- =============================================================================
-- EXERCICE 2 : SCRIPT ENTREPRISES DU DEPARTEMENT 74 (HAUTE-SAVOIE) CRÉÉES EN 2025
-- =============================================================================

USE base_sirene;

-- 1. REQUÊTE METIER INITIALE
-- Lister les Unités Légales (entreprises) ayant des établissements dans le 74 créés en 2025
SELECT DISTINCT ul.siren, ul.denomination, e.code_postal, e.date_creation
FROM unites_legales ul
JOIN etablissements e ON ul.siren = e.siren
WHERE e.code_departement = '74'
  AND e.date_creation >= '2025-01-01' 
  AND e.date_creation <= '2025-12-31';

-- 2. ANALYSE DU PLAN D'EXÉCUTION AVANT INDEXATION
EXPLAIN ANALYZE 
SELECT DISTINCT ul.siren, ul.denomination, e.code_postal, e.date_creation
FROM unites_legales ul
JOIN etablissements e ON ul.siren = e.siren
WHERE e.code_departement = '74'
  AND e.date_creation >= '2025-01-01' 
  AND e.date_creation <= '2025-12-31';

-- 3. CRÉATION DE L'INDEX COMPOSITE OPTIMAL
-- Index combinant le département et la plage de date de création (Covering Index)
CREATE INDEX idx_etab_dept_date_creation ON etablissements(code_departement, date_creation, siren);

-- 4. APPLIQUER ET VÉRIFIER L'USAGE DE L'INDEX DANS EXPLAIN ANALYZE
EXPLAIN ANALYZE 
SELECT DISTINCT ul.siren, ul.denomination, e.code_postal, e.date_creation
FROM unites_legales ul
JOIN etablissements e ON ul.siren = e.siren
WHERE e.code_departement = '74'
  AND e.date_creation >= '2025-01-01' 
  AND e.date_creation <= '2025-12-31';
