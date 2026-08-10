-- =============================================================================
-- EXERCICE 1 : OPTIMISATION ET AJOUT DES INDEX UTILES SUR LA BASE SIRENE
-- Formulaire de recherche : SIREN, SIRET, Code Postal, Département, Code Activité NAF
-- =============================================================================

USE base_sirene;

-- 1. ANALYSE AVANT INDEXATION (Exemple de requêtes lentes sans index)
EXPLAIN ANALYZE SELECT * FROM etablissements WHERE siret = '12345678901234';
EXPLAIN ANALYZE SELECT * FROM etablissements WHERE code_postal = '74000' AND code_activite = '6201Z';
EXPLAIN ANALYZE SELECT * FROM unites_legales WHERE siren = '123456789';

-- 2. AJOUT STRATÉGIQUE DES INDEX REQUIS POUR LE FORMULAIRE DE RECHERCHE

-- A. Index sur le numéro SIREN (Unités Légales & Établissements)
CREATE UNIQUE INDEX idx_unites_legales_siren ON unites_legales(siren);
CREATE INDEX idx_etablissements_siren ON etablissements(siren);

-- B. Index UNIQUE sur le numéro SIRET (Établissements)
CREATE UNIQUE INDEX idx_etablissements_siret ON etablissements(siret);

-- C. Index Composite sur Code Postal et Code Activité (Recherches fréquentes combinées)
CREATE INDEX idx_etablissements_cp_activite ON etablissements(code_postal, code_activite);

-- D. Index sur le Département (Extrait du code postal ou colonne dédiée)
CREATE INDEX idx_etablissements_departement ON etablissements(code_departement);

-- E. Index sur le Code Activité NAF/APE seul
CREATE INDEX idx_etablissements_code_activite ON etablissements(code_activite);

-- 3. ANALYSE APRÈS INDEXATION (Vérification du passage de 'ALL' à 'ref' / 'const')
EXPLAIN ANALYZE SELECT * FROM etablissements WHERE siret = '12345678901234';
EXPLAIN ANALYZE SELECT * FROM etablissements WHERE code_postal = '74000' AND code_activite = '6201Z';
