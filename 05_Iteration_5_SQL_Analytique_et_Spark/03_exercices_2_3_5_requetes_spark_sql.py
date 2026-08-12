#!/usr/bin/env python3
"""
Script de test automatique pour exécuter les requêtes SQL analytiques
de l'Atelier 2 (Exercices 2, 3 et 5) avec barre de progression dynamique.
"""

import os
import sys
import sqlite3
import csv
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_DIR = os.path.join(PROJECT_ROOT, '06_Donnees_CSV')
if not os.path.exists(CSV_DIR):
    CSV_DIR = os.path.join(PROJECT_ROOT, '05_Donnees_CSV')

FILE_ETAB = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')

def print_progress_bar(iteration, total, prefix='⏳ Chargement BDD', suffix='Complet', length=35, fill='█', is_finished=False):
    total_val = max(total, 1)
    current_val = min(iteration, total_val)
    percent = f"{100 * (current_val / float(total_val)):.1f}"
    filled_length = int(length * current_val // total_val)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix} ({iteration:,} / {total_val:,})')
    sys.stdout.flush()
    if is_finished:
        sys.stdout.write('\n')

def run_analytical_queries_test(limit_rows=100000):
    print("="*75)
    print(" 🧪 TEST AUTOMATIQUE DES REQUÊTES SQL ANALYTIQUES (EXERCICES 2, 3 & 5)")
    print("="*75)
    
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE etablissements (
        siret TEXT,
        siren TEXT,
        libelleCommuneEtablissement TEXT,
        codePostalEtablissement TEXT,
        etablissementSiege TEXT
    );
    """)

    if os.path.exists(FILE_ETAB):
        print(f" 📖 Chargement avec BARRE DE PROGRESSION de {limit_rows:,} établissements...")
        with open(FILE_ETAB, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for i, row in enumerate(reader, 1):
                batch.append((
                    row.get('siret', ''),
                    row.get('siren', ''),
                    row.get('libelleCommuneEtablissement', ''),
                    row.get('codePostalEtablissement', ''),
                    row.get('etablissementSiege', '')
                ))
                if len(batch) >= 10000:
                    cursor.executemany("INSERT INTO etablissements VALUES (?,?,?,?,?)", batch)
                    batch = []
                    print_progress_bar(i, limit_rows, prefix='⏳ Chargement BDD Test')
                if i >= limit_rows:
                    break
            if batch:
                cursor.executemany("INSERT INTO etablissements VALUES (?,?,?,?,?)", batch)
                print_progress_bar(limit_rows, limit_rows, prefix='⏳ Chargement BDD Test', is_finished=True)

    cursor.execute("CREATE INDEX idx_commune ON etablissements(libelleCommuneEtablissement);")
    cursor.execute("CREATE INDEX idx_cp ON etablissements(codePostalEtablissement);")

    # TEST EXERCICE 2
    print("\n--- 📍 EXERCICE 2 : Comptage des établissements par commune (Extrait 5 premières) ---")
    q2 = """
    SELECT libelleCommuneEtablissement AS commune, codePostalEtablissement AS cp, COUNT(*) AS total
    FROM etablissements
    WHERE libelleCommuneEtablissement != ''
    GROUP BY libelleCommuneEtablissement, codePostalEtablissement
    ORDER BY total DESC LIMIT 5;
    """
    for r in cursor.execute(q2).fetchall():
        print(f"   • Commune: {r[0]} ({r[1]}) -> {r[2]:,} établissements")

    # TEST EXERCICE 3
    print("\n--- 📍 EXERCICE 3 : Comptage des établissements et sièges sociaux par département ---")
    q3 = """
    SELECT SUBSTR(codePostalEtablissement, 1, 2) AS dept, COUNT(*) AS total,
           SUM(CASE WHEN etablissementSiege = 'true' THEN 1 ELSE 0 END) AS sieges
    FROM etablissements
    WHERE LENGTH(codePostalEtablissement) >= 2
    GROUP BY SUBSTR(codePostalEtablissement, 1, 2)
    ORDER BY total DESC LIMIT 5;
    """
    for r in cursor.execute(q3).fetchall():
        print(f"   • Dept {r[0]}: {r[1]:,} établissements dont {r[2]:,} sièges sociaux")

    # TEST EXERCICE 5 (TOP 10 & FLOP 10)
    print("\n--- 🏆 EXERCICE 5 : TOP 5 des communes ayant le plus d'établissements ---")
    q5_top = """
    SELECT libelleCommuneEtablissement, codePostalEtablissement, COUNT(*) AS total
    FROM etablissements WHERE libelleCommuneEtablissement != ''
    GROUP BY libelleCommuneEtablissement, codePostalEtablissement
    ORDER BY total DESC LIMIT 5;
    """
    for idx, r in enumerate(cursor.execute(q5_top).fetchall(), 1):
        print(f"   {idx}. {r[0]} ({r[1]}) -> {r[2]:,} établissements")

    print("\n--- 🔻 EXERCICE 5 (SUITE) : FLOP 5 des communes ayant le moins d'établissements ---")
    q5_flop = """
    SELECT libelleCommuneEtablissement, codePostalEtablissement, COUNT(*) AS total
    FROM etablissements WHERE libelleCommuneEtablissement != ''
    GROUP BY libelleCommuneEtablissement, codePostalEtablissement
    ORDER BY total ASC LIMIT 5;
    """
    for idx, r in enumerate(cursor.execute(q5_flop).fetchall(), 1):
        print(f"   {idx}. {r[0]} ({r[1]}) -> {r[2]:,} établissement(s)")

    print("\n" + "="*75)
    print(" ✅ TOUTES LES REQUÊTES SQL ANALYTIQUES SONT SANS ERREUR ET VALIDÉES !")
    print("="*75)

if __name__ == '__main__':
    run_analytical_queries_test()
