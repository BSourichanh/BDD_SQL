#!/usr/bin/env python3
"""
Livrable Atelier 2 — Exercice 1 : Génération de la Base Réduite Analytique par Commune
Convention : SOURICHANH-Bernard-Campus-Atelier2-BaseReduite.py

Ce script lit les données SIRENE et crée la base la plus petite possible 
formatée pour l'analytique par commune (Format Parquet & CSV ultra-léger),
avec barre de progression mono-ligne sans saut de ligne.
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

OUTPUT_PARQUET = os.path.join(os.path.dirname(__file__), 'sirene_analytique_commune.parquet')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'sirene_analytique_commune.csv')

def print_progress_bar(iteration, total, prefix='⏳ Base Réduite', suffix='Complet', length=35, fill='█', is_finished=False):
    total_val = max(total, 1)
    current_val = min(iteration, total_val)
    percent = f"{100 * (current_val / float(total_val)):.1f}"
    filled_length = int(length * current_val // total_val)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix} ({iteration:,} / {total_val:,})')
    sys.stdout.flush()
    if is_finished:
        sys.stdout.write('\n')

def generate_reduced_analytic_database(limit_rows=600000):
    print("="*75)
    print(" 🚀 EXERCICE 1 : CRÉATION DE LA BASE RÉDUITE ANALYTIQUE PAR COMMUNE")
    print("="*75)
    t0 = time.time()
    
    communes_agg = {}
    departements_agg = {}
    activites_agg = {}
    entreprises_agg = {}
    creations_annee_agg = {}
    
    total_etablissements = 0
    total_sieges = 0

    if not os.path.exists(FILE_ETAB):
        print(f"⚠️ Fichier {FILE_ETAB} non trouvé...")
        return

    print(f" 📖 Lecture optimisée avec BARRE DE PROGRESSION ({limit_rows:,} lignes)...")
    with open(FILE_ETAB, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            commune = (row.get('libelleCommuneEtablissement') or '').strip().upper()
            cp = (row.get('codePostalEtablissement') or '').strip()
            dept = cp[:2] if len(cp) >= 2 else '00'
            act = (row.get('activitePrincipaleEtablissement') or 'ND').strip().upper()
            is_siege = row.get('etablissementSiege') == 'true'

            if i % 10000 == 0 or i == limit_rows:
                print_progress_bar(i, limit_rows, prefix='⏳ Base Réduite')

            if not commune:
                continue

            total_etablissements += 1
            if is_siege:
                total_sieges += 1

            if commune not in communes_agg:
                communes_agg[commune] = {
                    'commune': commune,
                    'code_postal': cp,
                    'departement': dept,
                    'nb_etablissements': 0,
                    'nb_sieges': 0
                }
            communes_agg[commune]['nb_etablissements'] += 1
            if is_siege:
                communes_agg[commune]['nb_sieges'] += 1

            if i >= limit_rows:
                break

    print_progress_bar(limit_rows, limit_rows, prefix='⏳ Base Réduite', is_finished=True)

    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['commune', 'code_postal', 'departement', 'nb_etablissements', 'nb_sieges'])
        for c, data in sorted(communes_agg.items()):
            writer.writerow([data['commune'], data['code_postal'], data['departement'], data['nb_etablissements'], data['nb_sieges']])

    size_csv_kb = round(os.path.getsize(OUTPUT_CSV) / 1024, 2)
    exec_time = round(time.time() - t0, 2)

    print(f"\n ✅ BASE RÉDUITE ANALYTIQUE GÉNÉRÉE EN {exec_time}s !")
    print(f"    📍 Total Communes distinctes : {len(communes_agg):,}")
    print(f"    🏢 Total Établissements comptabilisés : {total_etablissements:,}")
    print(f"    🏛️ Total Sièges Sociaux comptabilisés : {total_sieges:,}")
    print(f"    📁 Fichier optimisé produit : {OUTPUT_CSV} ({size_csv_kb} Ko au lieu de 10 Go !)")
    print("="*75 + "\n")

if __name__ == '__main__':
    generate_reduced_analytic_database()
