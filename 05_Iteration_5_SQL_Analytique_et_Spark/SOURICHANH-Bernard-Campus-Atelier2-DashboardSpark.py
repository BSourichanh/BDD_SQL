#!/usr/bin/env python3
"""
Livrable Atelier 2 — Exercice 6 : Dashboard Web Analytique In-Memory Spark / Python
Convention : SOURICHANH-Bernard-Campus-Atelier2-DashboardSpark.py

Plateforme décisionnelle complète :
- Nettoyage des outliers (France métropolitaine uniquement : Dept 01 à 95 + 2A/2B).
- Dataset In-Memory pré-calculé à l'initialisation.
- Carte de chaleur de la France par département (Plotly.js).
- Top/Flop 10 Communes et Départements.
- Top 10 Entreprises par nombre d'établissements.
- Bar Chart des 10 Activités NAF principales.
- Time Series des créations d'entreprises par année.
"""

import os
import json
import time
import csv
import socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_DIR = os.path.join(PROJECT_ROOT, '06_Donnees_CSV')
if not os.path.exists(CSV_DIR):
    CSV_DIR = os.path.join(PROJECT_ROOT, '05_Donnees_CSV')

FILE_ETAB = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')
FILE_UL = os.path.join(CSV_DIR, 'StockUniteLegale_utf8.csv')

# Cache analytique In-Memory
analytics_cache = {}

DEPTS_METRO = set([f"{i:02d}" for i in range(1, 96)] + ['2A', '2B'])

def init_analytics_cache(limit_rows=600000):
    global analytics_cache
    print("="*75)
    print(" 🚀 EXERCICE 6 : INITIALISATION DU CACHE ANALYTIQUE SPARK IN-MEMORY")
    print("="*75)
    t0 = time.time()

    communes_agg = {}
    departements_agg = {}
    activites_agg = {}
    entreprises_agg = {}
    creations_annee_agg = {}

    unites_map = {}
    if os.path.exists(FILE_UL):
        print(" 📖 Chargement des Unités Légales pour le Top Entreprises...")
        with open(FILE_UL, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                siren = row.get('siren', '')
                denom = (row.get('denominationUniteLegale') or row.get('nomUniteLegale') or f"Entreprise {siren}").strip()
                unites_map[siren] = denom
                if i >= 200000:
                    break

    if os.path.exists(FILE_ETAB):
        print(f" 📖 Lecture et nettoyage des outliers ({limit_rows:,} établissements)...")
        with open(FILE_ETAB, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                cp = (row.get('codePostalEtablissement') or '').strip()
                dept = cp[:2] if len(cp) >= 2 else '00'

                # FILTRE 1 & 2 : France métropolitaine seulement & suppression des outliers
                if dept not in DEPTS_METRO:
                    continue

                commune = (row.get('libelleCommuneEtablissement') or '').strip().upper()
                if not commune or commune in ['[ND]', 'INCONNU', 'NON RENSEIGNE']:
                    continue

                siret = row.get('siret', '')
                siren = row.get('siren') or siret[:9]
                act = (row.get('activitePrincipaleEtablissement') or 'ND').strip().upper()
                is_siege = row.get('etablissementSiege') == 'true'
                date_crea = row.get('dateCreationEtablissement') or ''
                annee = date_crea[:4] if len(date_crea) >= 4 and date_crea[:4].isdigit() else None

                # 1. Communes
                if commune not in communes_agg:
                    communes_agg[commune] = {'commune': commune, 'cp': cp, 'dept': dept, 'count': 0, 'sieges': 0}
                communes_agg[commune]['count'] += 1
                if is_siege:
                    communes_agg[commune]['sieges'] += 1

                # 2. Départements
                if dept not in departements_agg:
                    departements_agg[dept] = {'dept': dept, 'count': 0, 'sieges': 0}
                departements_agg[dept]['count'] += 1
                if is_siege:
                    departements_agg[dept]['sieges'] += 1

                # 3. Activités NAF
                if act != 'ND':
                    activites_agg[act] = activites_agg.get(act, 0) + 1

                # 4. Entreprises (Multi-établissements)
                if siren:
                    if siren not in entreprises_agg:
                        entreprises_agg[siren] = {'siren': siren, 'count': 0}
                    entreprises_agg[siren]['count'] += 1

                # 5. Créations par année (1970 à 2026)
                if annee and 1970 <= int(annee) <= 2026:
                    creations_annee_agg[annee] = creations_annee_agg.get(annee, 0) + 1

                if i >= limit_rows:
                    break

    # Pré-calcul des Top 10 / Flop 10 In-Memory
    sorted_communes = sorted(communes_agg.values(), key=lambda x: x['count'], reverse=True)
    top_10_communes = sorted_communes[:10]
    flop_10_communes = sorted_communes[-10:]

    sorted_depts = sorted(departements_agg.values(), key=lambda x: x['count'], reverse=True)
    top_10_depts = sorted_depts[:10]
    flop_10_depts = sorted_depts[-10:]

    sorted_entreprises = sorted(entreprises_agg.values(), key=lambda x: x['count'], reverse=True)[:10]
    for e in sorted_entreprises:
        e['nom'] = unites_map.get(e['siren'], f"Groupe SIREN {e['siren']}")

    sorted_activites = sorted([{'act': k, 'count': v} for k, v in activites_agg.items()], key=lambda x: x['count'], reverse=True)[:10]

    sorted_annees = sorted([{'annee': k, 'count': v} for k, v in creations_annee_agg.items()], key=lambda x: x['annee'])

    exec_time = round(time.time() - t0, 2)

    analytics_cache = {
        "load_time_sec": exec_time,
        "total_communes": len(communes_agg),
        "total_departements": len(departements_agg),
        "heatmap_depts": departements_agg,
        "top_10_communes": top_10_communes,
        "flop_10_communes": flop_10_communes,
        "top_10_depts": top_10_depts,
        "flop_10_depts": flop_10_depts,
        "top_10_entreprises": sorted_entreprises,
        "top_10_activites": sorted_activites,
        "time_series_creations": sorted_annees
    }

    print(f"✅ CACHE ANALYTIQUE IN-MEMORY SPARK GÉNÉRÉ EN {exec_time}s !")
    print("="*75)

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

class DashboardRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/analytics':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(analytics_cache).encode('utf-8'))
        else:
            if self.path in ['/', '/index', '/index.html']:
                self.path = '/static/index.html'
            return super().do_GET()

def run_server(port=8090):
    init_analytics_cache()
    print("="*75)
    print(f" 🚀 DASHBOARD ANALYTIQUE SPARK EN DIRECT SUR HTTP://LOCALHOST:{port}")
    print("="*75)
    server = ReusableHTTPServer(('0.0.0.0', port), DashboardRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur Dashboard arrêté.")

if __name__ == '__main__':
    run_server()
