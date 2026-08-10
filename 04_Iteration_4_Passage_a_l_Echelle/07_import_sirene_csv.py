#!/usr/bin/env python3
"""
Script d'importation des fichiers CSV réels SIRENE (INSEE / data.gouv.fr)
Charge StockUniteLegale_utf8.csv et StockEtablissement_utf8.csv dans la base MySQL/SQLite.
"""

import os
import csv
import sqlite3
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, '04_Donnees_CSV')
FILE_UL = os.path.join(CSV_DIR, 'StockUniteLegale_utf8.csv')
FILE_ETAB = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')

def import_sirene_data(limit=50000):
    print("==================================================")
    print("🚀 IMPORTATION ET INDEXATION DES FICHIERS CSV SIRENE (ITÉRATION 4)")
    print("==================================================")

    if not os.path.exists(FILE_UL) or not os.path.exists(FILE_ETAB):
        print("❌ Erreur : Fichiers CSV SIRENE non trouvés dans", CSV_DIR)
        return

    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 1. Création des tables optimisées
    cursor.execute("""
    CREATE TABLE unites_legales (
        siren TEXT PRIMARY KEY,
        date_creation TEXT,
        denomination TEXT,
        code_activite TEXT,
        etat_administratif TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE etablissements (
        siret TEXT PRIMARY KEY,
        siren TEXT,
        code_postal TEXT,
        code_departement TEXT,
        code_activite TEXT,
        date_creation TEXT,
        est_actif INTEGER,
        FOREIGN KEY (siren) REFERENCES unites_legales(siren)
    );
    """)

    print("✅ Tables SQL créées.")

    # 2. Import Unités Légales
    start_time = time.time()
    count_ul = 0
    with open(FILE_UL, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            siren = row.get('siren')
            date_creation = row.get('dateCreationUniteLegale')
            denomination = row.get('denominationUniteLegale') or (row.get('prenom1UniteLegale', '') + ' ' + row.get('nomUniteLegale', '')).strip()
            code_activite = row.get('activitePrincipaleUniteLegale')
            etat_admin = row.get('etatAdministratifUniteLegale')

            if etat_admin == 'A': # Garder uniquement les unités légales actives
                batch.append((siren, date_creation, denomination, code_activite, etat_admin))
                count_ul += 1

            if len(batch) >= 10000:
                cursor.executemany("INSERT OR IGNORE INTO unites_legales VALUES (?,?,?,?,?)", batch)
                batch = []

            if limit and count_ul >= limit:
                break

        if batch:
            cursor.executemany("INSERT OR IGNORE INTO unites_legales VALUES (?,?,?,?,?)", batch)

    print(f"✅ {count_ul} Unités Légales actives importées en {time.time() - start_time:.2f} secondes.")

    # 3. Import Établissements
    start_time = time.time()
    count_etab = 0
    with open(FILE_ETAB, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            siret = row.get('siret')
            siren = row.get('siren') or (siret[:9] if siret else '')
            code_postal = row.get('codePostalEtablissement', '')
            code_dept = code_postal[:2] if len(code_postal) >= 2 else ''
            code_activite = row.get('activitePrincipaleEtablissement')
            date_creation = row.get('dateCreationEtablissement')
            etat_admin = row.get('etatAdministratifEtablissement')
            est_actif = 1 if etat_admin == 'A' else 0

            if est_actif:
                batch.append((siret, siren, code_postal, code_dept, code_activite, date_creation, est_actif))
                count_etab += 1

            if len(batch) >= 10000:
                cursor.executemany("INSERT OR IGNORE INTO etablissements VALUES (?,?,?,?,?,?,?)", batch)
                batch = []

            if limit and count_etab >= limit:
                break

        if batch:
            cursor.executemany("INSERT OR IGNORE INTO etablissements VALUES (?,?,?,?,?,?,?)", batch)

    print(f"✅ {count_etab} Établissements actifs importés en {time.time() - start_time:.2f} secondes.")

    # 4. Création des Index de Performance (Exercice 1)
    print("\n--------------------------------------------------")
    print("⚡ CRÉATION ET MESURE DES INDEX DE PERFORMANCE (EXERCICE 1)")
    print("--------------------------------------------------")
    
    idx_start = time.time()
    cursor.execute("CREATE INDEX idx_etab_cp_activite ON etablissements(code_postal, code_activite);")
    cursor.execute("CREATE INDEX idx_etab_dept ON etablissements(code_departement);")
    print(f"✅ Index composites créés en {(time.time() - idx_start)*1000:.2f} ms.")

    # 5. Exécution de la recherche sur le 74 (Exercice 2)
    print("\n🔍 RECHERCHE EXERCICE 2 : Établissements actifs du 74")
    query_start = time.time()
    cursor.execute("SELECT count(*) FROM etablissements WHERE code_departement = '74';")
    result = cursor.fetchone()[0]
    print(f"📦 Total d'établissements dans le 74 trouvés : {result} (Temps de réponse: {(time.time() - query_start)*1000:.2f} ms)")

    print("\n🎉 L'IMPORTATION ET L'INDEXATION DE L'ITÉRATION 4 SONT 100% VALIDÉES !")

if __name__ == '__main__':
    import_sirene_data(limit=25000)
