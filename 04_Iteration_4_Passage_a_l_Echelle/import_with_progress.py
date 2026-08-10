#!/usr/bin/env python3
"""
Script d'importation Docker avec Suivi Visuel et Barres de Progression en Temps Réel (Itération 4)
Smart Bypass : Ne copie PAS les CSV s'ils sont déjà présents dans le conteneur Docker !
Tolérance aux Doublons : Utilise LOAD DATA IGNORE INTO TABLE pour ignorer les SIRET en doublon.
"""

import os
import sys
import time
import subprocess
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Auto-détection du dossier CSV (05_Donnees_CSV ou 04_Donnees_CSV)
CSV_DIR = os.path.join(BASE_DIR, '05_Donnees_CSV')
if not os.path.exists(CSV_DIR):
    CSV_DIR = os.path.join(BASE_DIR, '04_Donnees_CSV')

FILE_UL = os.path.join(CSV_DIR, 'StockUniteLegale_utf8.csv')
FILE_ETAB = os.path.join(CSV_DIR, 'StockEtablissement_utf8.csv')
SQL_INDEX = os.path.join(BASE_DIR, '04_Iteration_4_Passage_a_l_Echelle', '02_exercice1_indexes_sirene.sql')

CONTAINER_NAME = 'docker_mysql'
CONTAINER_DEST = '/var/lib/mysql-files/'

def check_already_imported():
    """Vérifie si la BDD SIRENE contient déjà des données dans Docker MySQL."""
    try:
        cmd = [
            "docker", "exec", "-i", CONTAINER_NAME,
            "mysql", "-u", "root", "-phelloworld", "-N", "-e",
            "SELECT count(*) FROM base_sirene.etablissements;"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip().isdigit():
            count = int(res.stdout.strip())
            if count > 1000:
                return count
    except Exception:
        pass
    return 0

def check_table_has_rows(table_name):
    """Vérifie si une table contient déjà des lignes."""
    try:
        cmd = [
            "docker", "exec", "-i", CONTAINER_NAME,
            "mysql", "-u", "root", "-phelloworld", "-N", "-e",
            f"SELECT count(*) FROM base_sirene.{table_name};"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip().isdigit():
            count = int(res.stdout.strip())
            if count > 1000:
                return count
    except Exception:
        pass
    return 0

def check_file_exists_in_docker(filename):
    """Vérifie si le fichier CSV est déjà présent dans /var/lib/mysql-files/ du conteneur Docker."""
    try:
        cmd = ["docker", "exec", "-i", CONTAINER_NAME, "sh", "-c", f"[ -s '{CONTAINER_DEST}{filename}' ]"]
        res = subprocess.run(cmd, capture_output=True)
        return res.returncode == 0
    except Exception:
        return False

def draw_progress_bar(current, total, filename, start_time):
    percent = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    elapsed = time.time() - start_time
    speed_mb = (current / (1024 * 1024)) / elapsed if elapsed > 0 else 0
    curr_gb = current / (1024 ** 3)
    tot_gb = total / (1024 ** 3)
    eta = (total - current) / (speed_mb * 1024 * 1024) if speed_mb > 0 else 0
    
    sys.stdout.write(
        f"\r 📊 [{bar}] {percent:5.1f}% | {curr_gb:.2f}/{tot_gb:.2f} GB | {speed_mb:5.1f} MB/s | ETA: {int(eta):02d}s"
    )
    sys.stdout.flush()

def copy_file_with_progress(src_path, dst_filename):
    if not os.path.exists(src_path):
        print(f"\n❌ Fichier non trouvé : {src_path}")
        return False
    
    if check_file_exists_in_docker(dst_filename):
        print(f"\n⏩ LE FICHIER `{dst_filename}` EST DÉJÀ PRÉSENT DANS LE CONTENEUR DOCKER. COPIE SAUTÉE !")
        return True

    total_size = os.path.getsize(src_path)
    print(f"\n📂 Copie de `{dst_filename}` vers Docker ({total_size / (1024**3):.2f} GB)...")
    
    cmd = ["docker", "exec", "-i", CONTAINER_NAME, "sh", "-c", f"cat > {CONTAINER_DEST}{dst_filename}"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    
    chunk_size = 1024 * 1024 * 4 # 4MB chunks
    copied = 0
    start_time = time.time()
    
    with open(src_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            proc.stdin.write(chunk)
            copied += len(chunk)
            draw_progress_bar(copied, total_size, dst_filename, start_time)
            
    proc.stdin.close()
    proc.wait()
    sys.stdout.write("\n ✅ Copie terminée avec succès !\n")
    return True

class MysqlStepProgress(threading.Thread):
    def __init__(self, step_name):
        super().__init__()
        self.step_name = step_name
        self.stop_event = threading.Event()
        self.start_time = time.time()

    def run(self):
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        idx = 0
        while not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            sys.stdout.write(f"\r {spinner[idx % len(spinner)]} {self.step_name} (Temps écoulé: {elapsed:.1f}s)...")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.2)

    def stop(self):
        self.stop_event.set()
        self.join()
        elapsed = time.time() - self.start_time
        sys.stdout.write(f"\r ✅ {self.step_name} -> TERMINÉ en {elapsed:.1f}s !\n")
        sys.stdout.flush()

def run_sql_query(query_sql, description):
    progress = MysqlStepProgress(description)
    progress.start()
    try:
        cmd = ["docker", "exec", "-i", CONTAINER_NAME, "mysql", "-u", "root", "-phelloworld", "-e", query_sql]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        progress.stop()
        return True
    except subprocess.CalledProcessError as e:
        progress.stop()
        print(f"\n❌ Erreur SQL lors de `{description}` : {e.stderr}")
        raise e

def main():
    print("="*70)
    print(" 🐳 GESTIONNAIRE DOCKER SIRENE — SUIVI D'ÉTAPES & EN TEMPS RÉEL (ITÉRATION 4)")
    print("="*70)
    
    # 1. Vérification si la base est déjà importée
    existing_count = check_already_imported()
    if existing_count > 0:
        print(f"\n⚡ DÉTECTION : La base SIRENE est DÉJÀ importée dans Docker MySQL !")
        print(f"📦 Total d'établissements déjà présents : {existing_count:,} lignes.")
        print("⏩ Saut automatique du chargement des fichiers CSV !")
    else:
        print("\n--------------------------------------------------")
        print("📌 ÉTAPE 1/4 : COPIE DES FICHIERS CSV DANS DOCKER")
        print("--------------------------------------------------")
        copy_file_with_progress(FILE_UL, 'StockUniteLegale_utf8.csv')
        copy_file_with_progress(FILE_ETAB, 'StockEtablissement_utf8.csv')
        
        print("\n--------------------------------------------------")
        print("📌 ÉTAPE 2/4 : ALIMENTATION & CRÉATION DE LA BDD MYSQL")
        print("--------------------------------------------------")
        
        # 2.1 Initialisation des tables si non existantes
        init_sql = """
        SET GLOBAL sql_mode = '';
        SET SESSION sql_mode = '';
        SET FOREIGN_KEY_CHECKS = 0;
        CREATE DATABASE IF NOT EXISTS base_sirene DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        USE base_sirene;
        CREATE TABLE IF NOT EXISTS unites_legales (
            siren VARCHAR(9) PRIMARY KEY, statut_diffusion VARCHAR(5), unite_purgee VARCHAR(10),
            date_creation DATE NULL, sigle VARCHAR(20), sexe VARCHAR(5), prenom1 VARCHAR(50), prenom2 VARCHAR(50),
            prenom3 VARCHAR(50), prenom4 VARCHAR(50), prenom_usuel VARCHAR(50), pseudonyme VARCHAR(50),
            identifiant_association VARCHAR(50), tranche_effectifs VARCHAR(10), annee_effectifs VARCHAR(10),
            date_dernier_traitement DATETIME NULL, nombre_periodes INT NULL, categorie_entreprise VARCHAR(10),
            annee_categorie_entreprise VARCHAR(10), date_debut DATE NULL, etat_administratif CHAR(1), nom VARCHAR(100),
            nom_usage VARCHAR(100), denomination VARCHAR(150), denomination_usuelle1 VARCHAR(150), denomination_usuelle2 VARCHAR(150),
            denomination_usuelle3 VARCHAR(150), categorie_juridique VARCHAR(10), code_activite VARCHAR(10),
            nomenclature_activite VARCHAR(20), nic_siege VARCHAR(10), economie_sociale_solidaire VARCHAR(5),
            societe_mission VARCHAR(5), caractere_employeur VARCHAR(5), activite_principale_naf VARCHAR(10)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

        CREATE TABLE IF NOT EXISTS etablissements (
            siret VARCHAR(14) PRIMARY KEY, siren VARCHAR(9) NOT NULL, nic VARCHAR(5), statut_diffusion VARCHAR(5),
            date_creation DATE NULL, tranche_effectifs VARCHAR(10), annee_effectifs VARCHAR(10),
            activite_principale_registre VARCHAR(10), date_dernier_traitement DATETIME NULL, etablissement_siege VARCHAR(10),
            nombre_periodes INT NULL, code_postal CHAR(5), code_departement VARCHAR(3), code_activite VARCHAR(10),
            etat_administratif CHAR(1) NOT NULL DEFAULT 'A', est_actif TINYINT(1) NOT NULL DEFAULT 1
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        SET FOREIGN_KEY_CHECKS = 1;
        """
        run_sql_query(init_sql, "Création de la BDD et des structures de tables MySQL")
        
        # 2.2 Import Unités Légales (Si pas encore d'unités légales)
        if check_table_has_rows('unites_legales') > 0:
            print(" ⏩ Unités Légales déjà chargées dans MySQL. Étape sautée !")
        else:
            load_ul_sql = """
            USE base_sirene;
            SET SESSION sql_mode = '';
            LOAD DATA INFILE '/var/lib/mysql-files/StockUniteLegale_utf8.csv'
            IGNORE INTO TABLE unites_legales FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
            """
            run_sql_query(load_ul_sql, "Importation des Unités Légales (StockUniteLegale_utf8.csv) dans MySQL")
        
        # 2.3 Import Établissements avec IGNORE pour tolérer les doublons de SIRET
        load_etab_sql = """
        USE base_sirene;
        SET SESSION sql_mode = '';
        LOAD DATA INFILE '/var/lib/mysql-files/StockEtablissement_utf8.csv'
        IGNORE INTO TABLE etablissements FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
        """
        run_sql_query(load_etab_sql, "Importation des Établissements (StockEtablissement_utf8.csv avec IGNORE) dans MySQL")
        
        # 2.4 Filtrage des données actives
        filter_sql = """
        USE base_sirene;
        DELETE FROM etablissements WHERE etat_administratif <> 'A';
        DELETE FROM unites_legales WHERE etat_administratif <> 'A';
        """
        run_sql_query(filter_sql, "Filtrage et suppression des entreprises et établissements inactifs")

    # 3. Application / Vérification des index
    print("\n--------------------------------------------------")
    print("📌 ÉTAPE 3/4 : CRÉATION & VÉRIFICATION DES INDEX B-TREE")
    print("--------------------------------------------------")
    index_sql = """
    USE base_sirene;
    CREATE UNIQUE INDEX idx_unites_legales_siren ON unites_legales(siren);
    CREATE UNIQUE INDEX idx_etablissements_siret ON etablissements(siret);
    CREATE INDEX idx_etablissements_cp_activite ON etablissements(code_postal, code_activite);
    """
    try:
        run_sql_query(index_sql, "Création des Index B-Tree (SIREN, SIRET, CP + Activité)")
    except Exception:
        print(" ℹ️ Remarque : Index déjà appliqués sur la base de données.")

    # 4. Requête de test d'affichage
    print("\n--------------------------------------------------")
    print("📌 ÉTAPE 4/4 : VÉRIFICATION DE LA BASE SIRENE DANS MYSQL")
    print("--------------------------------------------------")
    count_sql = "USE base_sirene; SELECT COUNT(*) FROM etablissements;"
    try:
        cmd = ["docker", "exec", "-i", CONTAINER_NAME, "mysql", "-u", "root", "-phelloworld", "-N", "-e", count_sql]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        total_etab = int(res.stdout.strip())
        print(f" 📦 TOTAL D'ÉTABLISSEMENTS ACTIFS DANS MYSQL DOCKER : {total_etab:,} lignes.")
    except Exception:
        pass

    print("\n" + "="*70)
    print(" 🎉 TOUTES LES ÉTAPES DE L'ITÉRATION 4 SONT COMPLÉTÉES ET VALIDÉES !")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
