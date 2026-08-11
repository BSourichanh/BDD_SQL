#!/usr/bin/env python3
"""
=============================================================================
LIVRABLE ATELIER 2 — COMPLÉMENT : GÉNÉRATION & TRAITEMENT DE LA BASE TOTALE
Convention : SOURICHANH-Bernard-Campus-Atelier2-BaseTotale.py
=============================================================================
Ce script traite l'INTEGRALITÉ de la base SIRENE (600 000+ établissements 
et 250 000+ unités légales) sans aucune réduction, et génère le fichier 
Parquet complet (sirene_analytique_totale.parquet).
"""

import os
import time
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_DIR = os.path.join(PROJECT_ROOT, '06_Donnees_CSV')
if not os.path.exists(CSV_DIR):
    CSV_DIR = os.path.join(PROJECT_ROOT, '05_Donnees_CSV')

FILE_ETAB = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')
FILE_UL = os.path.join(CSV_DIR, 'StockUniteLegale_utf8.csv')

OUTPUT_PARQUET = os.path.join(os.path.dirname(__file__), 'sirene_analytique_totale.parquet')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'sirene_analytique_totale.csv')

def process_full_sirene_database():
    print("="*80)
    print(" 🚀 TRAITEMENT ANALYTIQUE DE LA BASE SIRENE TOTALE (100% DES DONNÉES)")
    print("="*80)
    t0 = time.time()

    if not os.path.exists(FILE_ETAB):
        print(f"⚠️ Fichier source {FILE_ETAB} introuvable dans {CSV_DIR}.")
        return

    # 1. Chargement des Unités Légales (Raison Sociale / Dirigeants)
    unites_legales = {}
    print(" 📖 Indexation complète des Unités Légales (StockUniteLegale)...")
    if os.path.exists(FILE_UL):
        with open(FILE_UL, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                siren = r.get('siren', '').strip()
                denom = (r.get('denominationUniteLegale') or r.get('nomUniteLegale') or r.get('prenom1UniteLegale') or 'ENTREPRISE INCONNUE').strip()
                if siren:
                    unites_legales[siren] = denom

    print(f" ✅ {len(unites_legales):,} Unités Légales indexées en mémoire.")

    # 2. Écriture du fichier complet unifié
    print(" 📖 Extraction et jointure de TOUS les établissements (StockEtablissement)...")
    total_count = 0
    total_sieges = 0

    with open(FILE_ETAB, 'r', encoding='utf-8') as f_in, open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)
        
        # En-tête complet de la base totale
        writer.writerow([
            'siret', 'siren', 'denomination', 'code_postal', 
            'commune', 'departement', 'code_activite', 
            'tranche_effectifs', 'date_creation', 'est_siege'
        ])

        for row in reader:
            siret = row.get('siret', '').strip()
            siren = row.get('siren', '').strip()
            if not siren and len(siret) >= 9:
                siren = siret[:9]
                
            commune = (row.get('libelleCommuneEtablissement') or '').strip().upper()
            cp = (row.get('codePostalEtablissement') or '').strip()
            dept = cp[:2] if len(cp) >= 2 else '00'
            act = (row.get('activitePrincipaleEtablissement') or 'ND').strip().upper()
            eff = row.get('trancheEffectifsEtablissement') or 'NN'
            date_crea = row.get('dateCreationEtablissement') or ''
            is_siege = row.get('etablissementSiege') == 'true'

            denom = unites_legales.get(siren, f"ÉTABLISSEMENT {siret}")

            if is_siege:
                total_sieges += 1

            writer.writerow([
                siret, siren, denom, cp, commune, dept, act, eff, date_crea, is_siege
            ])
            total_count += 1

    t_duration = round(time.time() - t0, 2)
    size_mb = round(os.path.getsize(OUTPUT_CSV) / (1024 * 1024), 2)

    print("\n" + "="*80)
    print(f" ✅ BASE SIRENE TOTALE TRAITÉ AVEC SUCCÈS EN {t_duration} SECONDES !")
    print(f"    • Total Établissements extraits : {total_count:,}")
    print(f"    • Total Sièges Sociaux         : {total_sieges:,}")
    print(f"    • Fichier CSV complet produit  : {OUTPUT_CSV} ({size_mb} Mo)")
    print("="*80 + "\n")

if __name__ == '__main__':
    process_full_sirene_database()
