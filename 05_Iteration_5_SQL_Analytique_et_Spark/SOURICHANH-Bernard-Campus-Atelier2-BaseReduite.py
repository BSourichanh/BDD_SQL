#!/usr/bin/env python3
"""
=============================================================================
LIVRABLE ATELIER 2 — ITÉRATION 5 : BASE RÉDUITE PAR COMMUNE (EXERCICE 1)
Convention : SOURICHANH-Bernard-Campus-Atelier2-BaseReduite.py
=============================================================================
Ce script filtre et agrège la Base Sirene brute (43,8M établissements)
pour produire un fichier CSV/Parquet analytique récapitulatif par commune.
"""

import os
import sys
import time
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_DIR = os.path.join(PROJECT_ROOT, '06_Donnees_CSV')
if not os.path.exists(CSV_DIR):
    CSV_DIR = os.path.join(PROJECT_ROOT, '05_Donnees_CSV')

INPUT_CSV = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'sirene_analytique_reduite.csv')

def print_progress_bar(iteration, total, prefix='⏳ Progress', suffix='Complet', length=35, fill='█', is_finished=False):
    total_val = max(total, 1)
    current_val = min(iteration, total_val)
    percent = f"{100 * (current_val / float(total_val)):.1f}"
    filled_length = int(length * current_val // total_val)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    if sys.stdout.isatty():
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix} ({current_val:,} / {total_val:,})')
        sys.stdout.flush()
        if is_finished:
            sys.stdout.write('\n')
    else:
        if is_finished or current_val % max(1, total_val // 10) == 0:
            sys.stdout.write(f'{prefix} |{bar}| {percent}% {suffix} ({current_val:,} / {total_val:,})\n')
            sys.stdout.flush()

def process_base_reduite():
    print("="*80)
    print(" 🚀 TRAITEMENT ANALYTIQUE DE LA BASE SIRENE RÉDUITE (EXERCICE 1)")
    print("="*80)
    t0 = time.time()

    if not os.path.exists(INPUT_CSV):
        print(f" ⚠️ Fichier source {INPUT_CSV} introuvable.")
        return

    communes_stats = {}
    total_lignes = 600000

    print(" 📖 Extraction et agrégation des établissements par commune...")
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            commune = (row.get('libelleCommuneEtablissement') or '').strip().upper()
            cp = (row.get('codePostalEtablissement') or '').strip()
            is_siege = (row.get('etablissementSiege') or '').lower() == 'true'

            if not commune or not cp:
                continue

            dept = cp[:2] if len(cp) >= 2 else '00'
            key = (commune, cp, dept)

            if key not in communes_stats:
                communes_stats[key] = {'total_etablissements': 0, 'total_sieges': 0}

            communes_stats[key]['total_etablissements'] += 1
            if is_siege:
                communes_stats[key]['total_sieges'] += 1

            if i % 25000 == 0:
                print_progress_bar(i, total_lignes, prefix='⏳ Base Réduite')

    print_progress_bar(total_lignes, total_lignes, prefix='⏳ Base Réduite', is_finished=True)

    print(" 💾 Écriture du fichier CSV analytique réduit...")
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['nom_commune', 'code_postal', 'departement', 'nombre_etablissements', 'nombre_sieges'])
        for (commune, cp, dept), stats in communes_stats.items():
            writer.writerow([commune, cp, dept, stats['total_etablissements'], stats['total_sieges']])

    exec_time = round(time.time() - t0, 2)
    size_kb = round(os.path.getsize(OUTPUT_CSV) / 1024, 2)

    print("\n" + "="*80)
    print(f" ✅ BASE RÉDUITE TRAITÉE AVEC SUCCÈS EN {exec_time} SECONDES !")
    print(f"    • Total Communes uniques : {len(communes_stats):,}")
    print(f"    • Fichier CSV produit    : {OUTPUT_CSV} ({size_kb} Ko)")
    print("="*80 + "\n")

if __name__ == '__main__':
    process_base_reduite()
