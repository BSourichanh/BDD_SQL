-- =============================================================================
-- SCRIPT DE REMPLISSAGE (JEU DE DONNÉES DE TEST) : bdd_colis_relais
-- Projet : Gestion de Livraison de Colis en Points Relais à Domicile
-- Version : 1.1 (Itération 1 - Harmonisé & Optimisé)
-- =============================================================================

USE bdd_colis_relais;

-- 1. INSERTION DES TRANSPORTEURS
INSERT INTO transporteurs (id_transporteur, nom_societe, siret, email_contact, telephone_contact, est_actif, date_partenariat) VALUES
(1, 'DHL Express France', '12345678901234', 'partenaires@dhl.fr', '0149754000', TRUE, '2025-01-10'),
(2, 'Chronopost', '98765432109876', 'relais@chronopost.fr', '0969391414', TRUE, '2025-02-01'),
(3, 'Mondial Relay', '45678912345678', 'reseau-particulier@mondialrelay.fr', '0969322332', TRUE, '2025-03-15');

-- 2. INSERTION DES CLIENTS
INSERT INTO clients (id_client, nom_client, prenom_client, email, telephone, adresse_rue, code_postal, ville) VALUES
(1, 'Dupont', 'Jean', 'jean.dupont@email.fr', '0612345678', '12 Avenue des Fleurs', '75011', 'Paris'),
(2, 'Curie', 'Marie', 'marie.curie@email.fr', '0698765432', '5 Rue de la Paix', '34000', 'Montpellier'),
(3, 'Martin', 'Thomas', 'thomas.martin@email.fr', '0755443322', '88 Boulevard Victor Hugo', '69002', 'Lyon'),
(4, 'Bernard', 'Sophie', 'sophie.bernard@email.fr', '0633221100', '3 Impasse des Lilas', '31000', 'Toulouse');

-- 3. INSERTION DES PARTICULIERS (POINTS RELAIS)
INSERT INTO particuliers (id_particulier, nom_particulier, prenom_particulier, email, telephone, adresse_rue, adresse_complement, code_postal, ville, type_logement, capacite_stockage_colis, disponibilites_description, statut_eligibilite, date_inscription) VALUES
(1, 'Lefebvre', 'Antoine', 'antoine.relais@email.fr', '0622334455', '14 Rue de la République', 'Bâtiment A, RDC', '75011', 'Paris', 'Appartement', 8, 'Du Lundi au Vendredi de 17h30 à 20h00, Samedi toute la journée', 'ACTIF', '2025-01-15 10:00:00'),
(2, 'Moreau', 'Camille', 'camille.relais@email.fr', '0677889900', '27 Chemin du Moulin', NULL, '34000', 'Montpellier', 'Maison', 15, 'Mardi au Samedi de 14h00 à 19h00', 'ACTIF', '2025-02-20 14:30:00'),
(3, 'Petit', 'Lucas', 'lucas.petit@email.fr', '0644556677', '9 Rue de la Gare', 'Apt 42', '69002', 'Lyon', 'Appartement', 4, 'Lundi, Mercredi, Vendredi de 18h00 à 21h00', 'EN_ATTENTE', '2025-07-01 09:15:00'),
(4, 'Dubois', 'Elodie', 'elodie.dubois@email.fr', '0611223344', '50 Rue Saint-Rome', NULL, '31000', 'Toulouse', 'Maison', 10, 'Disponible 7j/7 sur rendez-vous', 'SUSPENDU', '2025-03-10 11:20:00');

-- 4. INSERTION DES MISSIONS
INSERT INTO missions (id_mission, id_particulier, id_transporteur, date_debut, date_fin, statut_mission) VALUES
(1, 1, 1, '2025-02-01', '2026-12-31', 'EN_COURS'),
(2, 1, 2, '2025-03-01', '2026-12-31', 'EN_COURS'),
(3, 2, 2, '2025-03-01', '2026-12-31', 'EN_COURS'),
(4, 2, 3, '2025-04-01', '2026-12-31', 'EN_COURS');

-- 5. INSERTION DES COLIS (Test de tous les états du cycle de vie)
INSERT INTO colis (id_colis, code_suivi, poids_kg, longueur_cm, largeur_cm, hauteur_cm, est_fragile, id_transporteur, id_client, id_point_relais, statut_actuel, date_creation, date_depot_relais, date_limite_retrait, date_retrait) VALUES
-- Colis 1 : En cours de livraison par le transporteur
(1, 'COL-2026-001', 1.50, 20, 15, 10, FALSE, 1, 1, NULL, 'EN_COURS_LIVRAISON', '2026-08-03 08:00:00', NULL, NULL, NULL),

-- Colis 2 : Arrivé au point relais (il y a 3 jours, disponible au retrait)
(2, 'COL-2026-002', 3.20, 30, 20, 15, TRUE, 2, 2, 2, 'AU_POINT_RELAIS', '2026-08-01 10:00:00', '2026-08-01 16:30:00', '2026-08-15 16:30:00', NULL),

-- Colis 3 : Retiré avec succès par le client
(3, 'COL-2026-003', 0.80, 15, 10, 5, FALSE, 1, 1, 1, 'RETIRE', '2026-07-20 09:00:00', '2026-07-21 14:00:00', '2026-08-04 14:00:00', '2026-07-23 18:45:00'),

-- Colis 4 : Non réclamé après 14 jours (déposé le 15 juillet, limite dépassée au 29 juillet)
(4, 'COL-2026-004', 5.00, 40, 30, 25, FALSE, 2, 3, 2, 'NON_RECLAME', '2026-07-14 11:00:00', '2026-07-15 15:00:00', '2026-07-29 15:00:00', NULL),

-- Colis 5 : En processus de retour (en attente de récupération par le transporteur au relais)
(5, 'COL-2026-005', 2.10, 25, 20, 10, TRUE, 3, 4, 2, 'EN_RETOUR_TRANSPORTEUR', '2026-07-10 09:30:00', '2026-07-11 17:00:00', '2026-07-25 17:00:00', NULL),

-- Colis 6 : Processus complètement terminé (récupéré par le transporteur suite au non retrait)
(6, 'COL-2026-006', 4.50, 35, 25, 20, FALSE, 2, 1, 1, 'LIVRAISON_TERMINEE', '2026-07-01 08:00:00', '2026-07-02 14:00:00', '2026-07-16 14:00:00', '2026-07-19 11:30:00');

-- 6. INSERTION DE L'HISTORIQUE DES STATUTS
INSERT INTO historique_statuts_colis (id_colis, statut, date_changement, id_point_relais, id_transporteur, commentaire) VALUES
(1, 'EN_COURS_LIVRAISON', '2026-08-03 08:00:00', NULL, 1, 'Prise en charge par le hub DHL'),
(2, 'EN_COURS_LIVRAISON', '2026-08-01 10:00:00', NULL, 2, 'Prise en charge Chronopost'),
(2, 'AU_POINT_RELAIS', '2026-08-01 16:30:00', 2, 2, 'Déposé chez Camille Moreau. Client notifié.'),
(3, 'EN_COURS_LIVRAISON', '2026-07-20 09:00:00', NULL, 1, 'Prise en charge DHL'),
(3, 'AU_POINT_RELAIS', '2026-07-21 14:00:00', 1, 1, 'Déposé chez Antoine Lefebvre'),
(3, 'RETIRE', '2026-07-23 18:45:00', 1, NULL, 'Remis à Jean Dupont sur présentation d une pièce d identité'),
(4, 'EN_COURS_LIVRAISON', '2026-07-14 11:00:00', NULL, 2, 'En transit'),
(4, 'AU_POINT_RELAIS', '2026-07-15 15:00:00', 2, 2, 'Déposé au point relais'),
(4, 'NON_RECLAME', '2026-07-30 00:00:00', 2, NULL, 'Passage automatique en non réclamé : délai de 14j expiré'),
(5, 'EN_COURS_LIVRAISON', '2026-07-10 09:30:00', NULL, 3, 'En transit Mondial Relay'),
(5, 'AU_POINT_RELAIS', '2026-07-11 17:00:00', 2, 3, 'Déposé chez Camille Moreau'),
(5, 'NON_RECLAME', '2026-07-26 00:00:00', 2, NULL, 'Délai de 14j dépassé'),
(5, 'EN_RETOUR_TRANSPORTEUR', '2026-07-27 10:00:00', 2, 3, 'Étiquette de retour générée. En attente du chauffeur Mondial Relay.'),
(6, 'EN_COURS_LIVRAISON', '2026-07-01 08:00:00', NULL, 2, 'En transit'),
(6, 'AU_POINT_RELAIS', '2026-07-02 14:00:00', 1, 2, 'Déposé chez Antoine Lefebvre'),
(6, 'NON_RECLAME', '2026-07-17 00:00:00', 1, NULL, 'Non réclamé par le destinataire'),
(6, 'EN_RETOUR_TRANSPORTEUR', '2026-07-18 09:00:00', 1, 2, 'Demande de retour enregistrée'),
(6, 'LIVRAISON_TERMINEE', '2026-07-19 11:30:00', 1, 2, 'Colis récupéré par le chauffeur Chronopost. Processus clôturé.');
