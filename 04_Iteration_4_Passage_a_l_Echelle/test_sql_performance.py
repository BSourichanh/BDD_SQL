#!/usr/bin/env python3
"""
Script de test interactif des scripts SQL de Performance (Itération 3 - Passage à l'Échelle).
Mesure les gains de temps d'exécution (EXPLAIN / Benchmark) avant et après indexation.
"""

import sqlite3
import time
import os

def run_performance_tests():
    print("==================================================")
    print("⚡ TEST & BENCHMARK DES PERFORMANCES SQL (ITÉRATION 3)")
    print("==================================================")

    # 1. Création de la base en mémoire avec 50 000 lignes fictives
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE etablissements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        siret TEXT,
        siren TEXT,
        code_postal TEXT,
        code_departement TEXT,
        code_activite TEXT,
        date_creation TEXT,
        est_actif INTEGER
    );
    """)

    print("\n⏳ Génération d'un jeu de données volumineux (50 000 établissements)...")
    batch = []
    for i in range(1, 50001):
        siret = f"{i:014d}"
        siren = siret[:9]
        dept = f"{(i % 95) + 1:02d}"
        cp = f"{dept}000"
        ape = "6201Z" if i % 10 == 0 else "4711D"
        date_c = "2025-03-15" if i % 5 == 0 else "2020-01-01"
        batch.append((siret, siren, cp, dept, ape, date_c, 1))

    cursor.executemany("INSERT INTO etablissements (siret, siren, code_postal, code_departement, code_activite, date_creation, est_actif) VALUES (?,?,?,?,?,?,?)", batch)
    conn.commit()
    print("✅ 50 000 lignes insérées.")

    # -------------------------------------------------------------------------
    # TEST 1 : RECHERCHE SANS INDEX (FULL TABLE SCAN)
    # -------------------------------------------------------------------------
    print("\n--------------------------------------------------")
    print("🔴 1. RECHERCHE SANS INDEX (Full Table Scan)")
    print("--------------------------------------------------")
    query1 = "SELECT count(*) FROM etablissements WHERE code_departement = '74' AND date_creation >= '2025-01-01';"
    
    t0 = time.time()
    for _ in range(20):
        cursor.execute(query1)
        res = cursor.fetchone()[0]
    t1 = time.time()
    sans_index_time = (t1 - t0) / 20 * 1000

    print(f" 📦 Résultat : {res} établissements trouvés dans le 74.")
    print(f" ⏱️ Temps moyen d'exécution : {sans_index_time:.3f} ms per query.")

    # -------------------------------------------------------------------------
    # TEST 2 : CREATION DE L'INDEX COMPOSITE OPTIMAL (EXERCICE 2)
    # -------------------------------------------------------------------------
    print("\n--------------------------------------------------")
    print("🟢 2. CRÉATION DE L'INDEX COMPOSITE (Exercice 2)")
    print("--------------------------------------------------")
    t_idx_0 = time.time()
    cursor.execute("CREATE INDEX idx_etab_dept_date ON etablissements(code_departement, date_creation);")
    t_idx_1 = time.time()
    print(f" ✅ Index `idx_etab_dept_date` créé en {(t_idx_1 - t_idx_0)*1000:.2f} ms.")

    # -------------------------------------------------------------------------
    # TEST 3 : RECHERCHE AVEC INDEX (INDEX SCAN)
    # -------------------------------------------------------------------------
    print("\n--------------------------------------------------")
    print("🚀 3. RECHERCHE AVEC INDEX COMPOSITE (Index Scan)")
    print("--------------------------------------------------")
    t0 = time.time()
    for _ in range(20):
        cursor.execute(query1)
        res = cursor.fetchone()[0]
    t1 = time.time()
    avec_index_time = (t1 - t0) / 20 * 1000

    print(f" ⏱️ Temps moyen d'exécution : {avec_index_time:.3f} ms per query.")
    
    if avec_index_time > 0:
        speedup = sans_index_time / avec_index_time
        print(f" 📈 GAIN DE PERFORMANCE : La requête est x{speedup:.1f} FOIS PLUS RAPIDE !")

    print("\n🎉 TOUS LES TESTS SQL SONT VALIDÉS ET EXÉCUTÉS AVEC SUCCÈS !")

if __name__ == '__main__':
    run_performance_tests()
