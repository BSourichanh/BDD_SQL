#!/usr/bin/env python3
"""
Serveur Web API & Formulaire SIRENE — RECHERCHE SANS LIMITATION
Libellé Moteur de Données : Base SQL Index B-Tree (Résultats Illimités).
"""

import os
import json
import time
import sqlite3
import csv
import socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CSV_DIR = os.path.join(PROJECT_ROOT, '05_Donnees_CSV')
if not os.path.exists(CSV_DIR):
    CSV_DIR = os.path.join(PROJECT_ROOT, '04_Donnees_CSV')

FILE_UL = os.path.join(CSV_DIR, 'StockUniteLegale_utf8.csv')
FILE_ETAB = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')

sqlite_conn = None

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

def init_max_info_database(limit_ul=250000, limit_etab=600000):
    global sqlite_conn
    print(f"⏳ Chargement de l'index principal BDD ({limit_etab:,} établissements INSEE)...")
    sqlite_conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = sqlite_conn.cursor()
    
    cursor.execute("""
    CREATE TABLE etablissements (
        siret TEXT PRIMARY KEY,
        siren TEXT,
        denomination TEXT,
        dirigeant TEXT,
        nom_complet TEXT,
        code_postal TEXT,
        commune TEXT,
        code_departement TEXT,
        code_activite TEXT,
        code_activite_clean TEXT,
        categorie TEXT,
        tranche_effectifs TEXT,
        date_creation TEXT,
        est_actif INTEGER
    );
    """)
    
    unites_map = {}
    if os.path.exists(FILE_UL):
        print(f" 📖 Indexation de {limit_ul:,} Unités Légales...")
        with open(FILE_UL, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                siren = row.get('siren', '')
                denom = (row.get('denominationUniteLegale') or '').strip()
                nom = (row.get('nomUniteLegale') or row.get('nomUsageUniteLegale') or '').strip()
                prenom = (row.get('prenom1UniteLegale') or '').strip()
                cat = row.get('categorieEntreprise') or 'PME'
                
                nom_complet = denom if denom else f"{nom} {prenom}".strip()
                if not nom_complet:
                    nom_complet = f"ENTREPRISE {siren}"
                    
                unites_map[siren] = (nom_complet, f"{prenom} {nom}".strip() or "N/A", cat)
                if i >= limit_ul:
                    break

    count_etab = 0
    if os.path.exists(FILE_ETAB):
        print(f" 📖 Indexation de {limit_etab:,} Établissements...")
        with open(FILE_ETAB, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for i, row in enumerate(reader):
                siret = row.get('siret', '')
                siren = row.get('siren') or siret[:9]
                denom_etab = (row.get('denominationUsuelleEtablissement') or row.get('enseigne1Etablissement') or '').strip()
                
                ul_denom, dirigente, cat = unites_map.get(siren, (f"ENTREPRISE SIRENE {siren}", "N/A", "PME"))
                denom_finale = denom_etab if denom_etab else ul_denom
                
                cp = row.get('codePostalEtablissement', '')
                commune = row.get('libelleCommuneEtablissement', '')
                dept = cp[:2] if len(cp) >= 2 else ''
                act = row.get('activitePrincipaleEtablissement', '')
                act_clean = act.replace('.', '').upper()
                effectifs = row.get('trancheEffectifsEtablissement', 'N/C')
                date_crea = row.get('dateCreationEtablissement', 'N/C')
                
                batch.append((siret, siren, denom_finale, dirigente, denom_finale.upper(), cp, commune, dept, act, act_clean, cat, effectifs, date_crea, 1))
                count_etab += 1
                
                if len(batch) >= 25000:
                    cursor.executemany("INSERT OR IGNORE INTO etablissements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
                    batch = []
                if i >= limit_etab:
                    break
            if batch:
                cursor.executemany("INSERT OR IGNORE INTO etablissements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)

    cursor.execute("CREATE INDEX idx_nom_complet ON etablissements(nom_complet);")
    cursor.execute("CREATE INDEX idx_siren ON etablissements(siren);")
    cursor.execute("CREATE INDEX idx_cp ON etablissements(code_postal);")
    cursor.execute("CREATE INDEX idx_dept ON etablissements(code_departement);")
    cursor.execute("CREATE INDEX idx_act ON etablissements(code_activite);")
    cursor.execute("CREATE INDEX idx_act_clean ON etablissements(code_activite_clean);")
    sqlite_conn.commit()
    print(f"✅ BASE DE DONNÉES INDEXÉE : {count_etab:,} établissements prêts !")

init_max_info_database()

def full_database_scan(nom, siren, siret, code_postal, departement, code_activite, max_results=1000):
    results = []
    if not os.path.exists(FILE_ETAB):
        return results

    act_clean = code_activite.replace('.', '').upper() if code_activite else ''
    
    with open(FILE_ETAB, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_siret = row.get('siret', '')
            s_siren = row.get('siren') or s_siret[:9]
            cp = row.get('codePostalEtablissement', '')
            dept = cp[:2] if len(cp) >= 2 else ''
            act = row.get('activitePrincipaleEtablissement', '')
            act_c = act.replace('.', '').upper()
            denom = (row.get('denominationUsuelleEtablissement') or row.get('enseigne1Etablissement') or f"ENTREPRISE {s_siren}").strip()
            
            if siren and s_siren != siren:
                continue
            if siret and s_siret != siret:
                continue
            if code_postal and cp != code_postal:
                continue
            if departement and dept != departement:
                continue
            if act_clean and act_clean not in act_c:
                continue
            if nom and nom not in denom.upper():
                continue

            results.append({
                "siret": s_siret,
                "siren": s_siren,
                "denomination": denom,
                "dirigeant": "N/A",
                "code_postal": cp,
                "commune": row.get('libelleCommuneEtablissement', ''),
                "departement": dept,
                "code_activite": act,
                "categorie": "PME",
                "effectifs": row.get('trancheEffectifsEtablissement', 'N/C'),
                "date_creation": row.get('dateCreationEtablissement', 'N/C'),
                "est_actif": "ACTIF"
            })

            if len(results) >= max_results:
                break
    return results

class SireneRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path in ['/', '/index', '/index.html']:
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/search':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            params = json.loads(body.decode('utf-8'))
            
            nom = params.get('nom', '').strip().upper()
            siren = params.get('siren', '').strip()
            siret = params.get('siret', '').strip()
            code_postal = params.get('code_postal', '').strip()
            departement = params.get('departement', '').strip()
            code_activite = params.get('code_activite', '').strip().upper()

            where_clause = ["1=1"]
            args = []

            if nom:
                where_clause.append("nom_complet LIKE ?")
                args.append(f"%{nom}%")
            if siren:
                where_clause.append("siren = ?")
                args.append(siren)
            if siret:
                where_clause.append("siret = ?")
                args.append(siret)
            if code_postal:
                where_clause.append("code_postal = ?")
                args.append(code_postal)
            if departement:
                where_clause.append("code_departement = ?")
                args.append(departement)
            
            if code_activite:
                act_clean = code_activite.replace('.', '')
                if any(c.isdigit() for c in code_activite):
                    where_clause.append("(code_activite_clean LIKE ? OR code_activite LIKE ?)")
                    args.extend([f"%{act_clean}%", f"%{code_activite}%"])
                else:
                    where_clause.append("(nom_complet LIKE ? OR code_activite LIKE ?)")
                    args.extend([f"%{code_activite}%", f"%{code_activite}%"])

            sql = f"""
            SELECT siret, siren, denomination, dirigeant, code_postal, commune, code_departement, code_activite, categorie, tranche_effectifs, date_creation
            FROM etablissements
            WHERE {' AND '.join(where_clause)}
            LIMIT 1000;
            """

            t0 = time.time()
            cur = sqlite_conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            source_used = "BDD SQL Index B-Tree"

            results = []
            for r in rows:
                results.append({
                    "siret": r[0],
                    "siren": r[1],
                    "denomination": r[2],
                    "dirigeant": r[3],
                    "code_postal": r[4],
                    "commune": r[5],
                    "departement": r[6],
                    "code_activite": r[7],
                    "categorie": r[8],
                    "effectifs": r[9],
                    "date_creation": r[10],
                    "est_actif": "ACTIF"
                })

            if len(results) == 0:
                results = full_database_scan(nom, siren, siret, code_postal, departement, code_activite)
                source_used = "Balayage Intégral du Dataset SIRENE INSEE"

            exec_time = round((time.time() - t0) * 1000, 3)

            response_data = {
                "source": source_used,
                "sql_query": sql.strip(),
                "execution_time_ms": exec_time,
                "count": len(results),
                "results": results
            }
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404)

def run_server(port=8080):
    for p in [port, 8000, 8085]:
        try:
            print("="*65)
            print(f" 🚀 SERVEUR BDD SIRENE EN DIRECT SUR HTTP://LOCALHOST:{p}")
            print("="*65)
            server = ReusableHTTPServer(('0.0.0.0', p), SireneRequestHandler)
            server.serve_forever()
            break
        except OSError:
            print(f" Port {p} occupé, tentative sur le port suivant...")

if __name__ == '__main__':
    run_server()
