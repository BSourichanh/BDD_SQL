-- =============================================================================
-- LIVRABLE ATELIER 2 — REQUÊTES ANALYTIQUES (EXERCICES 2, 3 ET 5)
-- Convention : SOURICHANH-Bernard-Campus-Atelier2-ComptagesAnalytiques.sql
-- =============================================================================

-- -----------------------------------------------------------------------------
-- EXERCICE 2 : COMPTER LE NOMBRE D'ÉTABLISSEMENTS PAR COMMUNE
-- -----------------------------------------------------------------------------
SELECT 
    libelleCommuneEtablissement AS commune,
    codePostalEtablissement AS code_postal,
    COUNT(*) AS nb_etablissements
FROM etablissements
WHERE libelleCommuneEtablissement IS NOT NULL AND libelleCommuneEtablissement != ''
GROUP BY libelleCommuneEtablissement, codePostalEtablissement
ORDER BY nb_etablissements DESC;


-- -----------------------------------------------------------------------------
-- EXERCICE 3 : COMPTER LE NOMBRE D'ÉTABLISSEMENTS ET SIÈGES SOCIAUX PAR DÉPARTEMENT
-- -----------------------------------------------------------------------------
SELECT 
    SUBSTRING(codePostalEtablissement, 1, 2) AS code_departement,
    COUNT(*) AS total_etablissements,
    SUM(CASE WHEN etablissementSiege = 'true' THEN 1 ELSE 0 END) AS total_sieges_sociaux
FROM etablissements
WHERE codePostalEtablissement IS NOT NULL AND CHAR_LENGTH(codePostalEtablissement) >= 2
GROUP BY SUBSTRING(codePostalEtablissement, 1, 2)
ORDER BY total_etablissements DESC;


-- -----------------------------------------------------------------------------
-- EXERCICE 5 : EXTRAIRE LES 10 COMMUNES QUI ONT LE PLUS D'ÉTABLISSEMENTS (TOP 10)
-- -----------------------------------------------------------------------------
-- Top 10 Communes (Les plus représentées)
SELECT 
    libelleCommuneEtablissement AS commune,
    codePostalEtablissement AS code_postal,
    COUNT(*) AS total_etablissements
FROM etablissements
WHERE libelleCommuneEtablissement IS NOT NULL AND libelleCommuneEtablissement != ''
GROUP BY libelleCommuneEtablissement, codePostalEtablissement
ORDER BY total_etablissements DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- EXERCICE 5 (SUITE) : EXTRAIRE LES 10 COMMUNES QUI ONT LE MOINS D'ÉTABLISSEMENTS (FLOP 10)
-- -----------------------------------------------------------------------------
-- Flop 10 Communes (Les moins représentées avec au moins 1 établissement)
SELECT 
    libelleCommuneEtablissement AS commune,
    codePostalEtablissement AS code_postal,
    COUNT(*) AS total_etablissements
FROM etablissements
WHERE libelleCommuneEtablissement IS NOT NULL AND libelleCommuneEtablissement != ''
GROUP BY libelleCommuneEtablissement, codePostalEtablissement
ORDER BY total_etablissements ASC
LIMIT 10;
