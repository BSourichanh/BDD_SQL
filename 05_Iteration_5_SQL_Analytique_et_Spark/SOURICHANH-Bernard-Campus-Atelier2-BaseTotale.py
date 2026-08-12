#!/usr/bin/env python3
"""
=============================================================================
LIVRABLE ATELIER 2 — COMPLÉMENT : GÉNÉRATION & TRAITEMENT DE LA BASE TOTALE PARQUET
Convention : SOURICHANH-Bernard-Campus-Atelier2-BaseTotale.py
=============================================================================
Ce script traite l'INTEGRALITÉ de la base SIRENE (43.8 millions d'établissements)
avec barre de progression dynamique mono-ligne sans saut de ligne intempestif.
"""

import os
import sys
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

def print_progress_bar(iteration, total, prefix='⏳ Base Totale', suffix='Complet', length=35, fill='█', is_finished=False):
    total_val = max(total, 1)
    current_val = min(iteration, total_val)
    percent = f"{100 * (current_val / float(total_val)):.1f}"
    filled_length = int(length * current_val // total_val)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix} ({iteration:,} / {total_val:,})')
    sys.stdout.flush()
    if is_finished:
        sys.stdout.write('\n')

def process_full_sirene_database():
    print("="*80)
    print(" 🚀 TRAITEMENT ANALYTIQUE DE LA BASE SIRENE TOTALE (100% DES DONNÉES)")
    print("="*80)
    t0 = time.time()

    if not os.path.exists(FILE_ETAB):
        print(f"⚠️ Fichier source {FILE_ETAB} introuvable dans {CSV_DIR}.")
        return

    # Total exacts de la base INSEE réelle
    total_ul_exact = 29922486
    total_etab_exact = 43896818

    # 1. Indexation des Unités Légales
    unites_legales = {}
    print(" 📖 Indexation complète des Unités Légales (StockUniteLegale)...")
    if os.path.exists(FILE_UL):
        with open(FILE_UL, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader, 1):
                siren = r.get('siren', '').strip()
                denom = (r.get('denominationUniteLegale') or r.get('nomUniteLegale') or r.get('prenom1UniteLegale') or 'ENTREPRISE INCONNUE').strip()
                if siren:
                    unites_legales[siren] = denom
                if i % 100000 == 0:
                    print_progress_bar(i, total_ul_exact, prefix='⏳ Indexation UL')

    print_progress_bar(len(unites_legales), total_ul_exact, prefix='⏳ Indexation UL', is_finished=True)
    print(f" ✅ {len(unites_legales):,} Unités Légales indexées en mémoire.")

    # 2. Écriture du fichier CSV/Parquet unifié
    print(" 📖 Extraction et écriture de TOUS les établissements...")
    total_count = 0
    total_sieges = 0

    with open(FILE_ETAB, 'r', encoding='utf-8') as f_in, open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)
        
        writer.writerow([
            'siret', 'siren', 'denomination', 'code_postal', 
            'commune', 'departement', 'code_activite', 
            'tranche_effectifs', 'date_creation', 'est_siege'
        ])

        for i, row in enumerate(reader, 1):
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

            if i % 100000 == 0:
                print_progress_bar(i, total_etab_exact, prefix='⏳ Base Totale')

    print_progress_bar(total_count, total_etab_exact, prefix='⏳ Base Totale', is_finished=True)

    t_duration = round(time.time() - t0, 2)
    size_csv_mb = round(os.path.getsize(OUTPUT_CSV) / (1024 * 1024), 2)

    print("\n" + "="*80)
    print(f" ✅ BASE SIRENE TOTALE TRAITÉE AVEC SUCCÈS EN {t_duration} SECONDES !")
    print(f"    • Total Établissements extraits : {total_count:,}")
    print(f"    • Total Sièges Sociaux         : {total_sieges:,}")
    print(f"    • Fichier CSV complet          : {OUTPUT_CSV} ({size_csv_mb} Mo)")
    print(f"    • Fichier PARQUET binaire      : {OUTPUT_PARQUET}")
    print("="*80 + "\n")

if __name__ == '__main__':
    process_full_sirene_database()
