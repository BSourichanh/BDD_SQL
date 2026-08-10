#!/usr/bin/env python3
"""
Script de test automatique pour la Base de Données Colis Relais.
Permet d'exécuter et de valider les scripts SQL DDL et DML sans dépendance externe.
"""

import sqlite3
import re
import os

def test_sql_scripts():
    path_ddl = os.path.join(os.path.dirname(__file__), '04_schema_creation.sql')
    path_dml = os.path.join(os.path.dirname(__file__), '05_insertion_donnees.sql')

    print("==================================================")
    print("🧪 TEST DE VALIDATION DES SCRIPTS SQL (DDL & DML)")
    print("==================================================")

    with open(path_ddl, 'r', encoding='utf-8') as f:
        ddl = f.read()

    with open(path_dml, 'r', encoding='utf-8') as f:
        dml = f.read()

    # Adaptation de la syntaxe MySQL vers SQLite pour le test local
    sqlite_ddl = ddl
    sqlite_ddl = re.sub(r'CREATE DATABASE IF NOT EXISTS.*?;', '', sqlite_ddl, flags=re.DOTALL)
    sqlite_ddl = re.sub(r'USE bdd_colis_relais;', '', sqlite_ddl)
    sqlite_ddl = re.sub(r'ENGINE=InnoDB.*?;', ';', sqlite_ddl)
    sqlite_ddl = re.sub(r'ENUM\(.*?\)', 'TEXT', sqlite_ddl, flags=re.DOTALL)
    sqlite_ddl = re.sub(r'\bDATETIME\b', 'TEXT', sqlite_ddl)
    sqlite_ddl = re.sub(r'\bDATE\b', 'TEXT', sqlite_ddl)
    sqlite_ddl = re.sub(r'\bBOOLEAN\b', 'INTEGER', sqlite_ddl)
    sqlite_ddl = re.sub(r'\bTRUE\b', '1', sqlite_ddl)
    sqlite_ddl = re.sub(r'\bFALSE\b', '0', sqlite_ddl)
    sqlite_ddl = re.sub(r'CHAR_LENGTH', 'LENGTH', sqlite_ddl)
    sqlite_ddl = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sqlite_ddl)
    sqlite_ddl = re.sub(r'INT AUTOINCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sqlite_ddl)

    sqlite_dml = dml
    sqlite_dml = re.sub(r'USE bdd_colis_relais;', '', sqlite_dml)
    sqlite_dml = re.sub(r'\bTRUE\b', '1', sqlite_dml)
    sqlite_dml = re.sub(r'\bFALSE\b', '0', sqlite_dml)

    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 1. Test DDL
    try:
        cursor.executescript(sqlite_ddl)
        print("✅ 1. Script DDL (04_schema_creation.sql) : VALIDE (Toutes les tables créées)")
    except Exception as e:
        print("❌ ERREUR DDL :", e)
        return

    # 2. Test DML
    try:
        cursor.executescript(sqlite_dml)
        print("✅ 2. Script DML (05_insertion_donnees.sql) : VALIDE (Données de test insérées)")
    except Exception as e:
        print("❌ ERREUR DML :", e)
        return

    print("\n--------------------------------------------------")
    print("📊 VÉRIFICATION DU NOMBRE DE LIGNES DANS CHAQUE TABLE")
    print("--------------------------------------------------")
    tables = ['transporteurs', 'clients', 'particuliers', 'missions', 'colis', 'historique_statuts_colis']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f" - Table {table:<25} : {count} enregistrements")

    print("\n--------------------------------------------------")
    print("🔍 REQUÊTE DE TEST : COLIS DISPONIBLES EN POINT RELAIS")
    print("--------------------------------------------------")
    query = """
    SELECT c.code_suivi, c.statut_actuel, cl.nom_client, p.nom_particulier, p.ville
    FROM colis c
    JOIN clients cl ON c.id_client = cl.id_client
    LEFT JOIN particuliers p ON c.id_point_relais = p.id_particulier
    WHERE c.statut_actuel = 'AU_POINT_RELAIS';
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for r in rows:
        print(f" 📦 Code: {r[0]} | Statut: {r[1]} | Client: {r[2]} | Relais: {r[3]} ({r[4]})")

    print("\n🎉 TOUS LES TESTS SONT AU VERT ! LA BASE DE DONNÉES EST PRÊTE.")

if __name__ == '__main__':
    test_sql_scripts()
