-- =============================================================================
-- LIVRABLE ATELIER 2 — ITÉRATION 6 : SCHÉMA BDD VECTORIELLE MARIADB 11 / SQL
-- Convention : SOURICHANH-Bernard-Campus-Atelier2-BodaccVectorSchema.sql
-- =============================================================================

USE sirene_db;

-- 1. Création de la table des annonces et jugements BODACC avec colonne VECTOR(384)
CREATE TABLE IF NOT EXISTS bodacc_jugements (
    id_annonce INT AUTO_INCREMENT PRIMARY KEY,
    siren VARCHAR(9) NOT NULL,
    siret VARCHAR(14),
    date_jugement DATE NOT NULL,
    type_procedure VARCHAR(100) NOT NULL,
    tribunal VARCHAR(150),
    detail_jugement TEXT NOT NULL,
    -- Colonne vectorielle 384 dimensions (Compatible MariaDB 11 VECTOR / PgVector)
    vector_embedding VECTOR(384),
    INDEX idx_bodacc_siren (siren),
    INDEX idx_bodacc_date (date_jugement),
    FOREIGN KEY (siren) REFERENCES etablissements(siren) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Insertion d'exemple de procédure collective BODACC avec vecteur d'embedding 384d
INSERT INTO bodacc_jugements (siren, siret, date_jugement, type_procedure, tribunal, detail_jugement, vector_embedding)
VALUES (
    '104062153',
    '10406215300012',
    '2026-01-15',
    'Redressement Judiciaire',
    'Tribunal de Commerce de Paris',
    'Ouverture d une procedure de redressement judiciaire pour cessation de paiements boulangerie.',
    VEC_FromText('[0.024, -0.158, 0.089, 0.412, -0.052, 0.118, -0.321, 0.005]')
);

-- 3. Requête SQL de recherche par similarité cosinus (Distance Vectorielle)
-- Recherche des jugements les plus similaires à une requête vectorielle d'entrée
SELECT 
    b.id_annonce,
    b.siren,
    e.denomination,
    b.type_procedure,
    b.tribunal,
    b.detail_jugement,
    VEC_DISTANCE_COSINE(b.vector_embedding, VEC_FromText('[0.024, -0.158, 0.089, 0.412, -0.052, 0.118, -0.321, 0.005]')) AS distance_vectorielle
FROM bodacc_jugements b
JOIN etablissements e ON b.siren = e.siren
ORDER BY distance_vectorielle ASC
LIMIT 10;
