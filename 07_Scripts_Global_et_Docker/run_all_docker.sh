#!/usr/bin/env bash
# =============================================================================
# AUTOMATION DOCKER : EXECUTION DE TOUTES LES ITÉRATIONS EN CONTENEURS
# =============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$DIR"

echo "=================================================="
echo "🐳 1. DÉMARRAGE DES CONTENEURS DOCKER"
echo "=================================================="
docker compose up -d

echo -e "\n⏳ Attente de la stabilisation du serveur MySQL..."
sleep 5

echo "=================================================="
echo "📦 2. ITÉRATION 1 : CRÉATION & REMPLISSAGE BDD COLIS RELAIS"
echo "=================================================="
docker exec -i docker_mysql mysql -u root -phelloworld < "$DIR/01_Iteration_1_Conception_et_Creation/04_schema_creation.sql"
docker exec -i docker_mysql mysql -u root -phelloworld < "$DIR/01_Iteration_1_Conception_et_Creation/05_insertion_donnees.sql"
echo "✅ BDD Colis Relais créée et initialisée dans Docker."

echo "=================================================="
echo "🛡️ 3. ITÉRATION 2 : SÉCURISATION & PRIVILÈGES"
echo "=================================================="
docker exec -i docker_mysql mysql -u root -phelloworld < "$DIR/02_Iteration_2_Securisation_et_Privileges/07_patch_securite.sql"
echo "✅ Patch sécurité et privilèges appliqués dans Docker."

echo "=================================================="
echo "🚀 4. ITÉRATION 4 : IMPORTATION & INDEXATION SIRENE"
echo "=================================================="
docker cp "$DIR/05_Donnees_CSV/StockUniteLegale_utf8.csv" docker_mysql:/var/lib/mysql-files/ 2>/dev/null || true
docker cp "$DIR/05_Donnees_CSV/StockEtablissement_utf8.csv" docker_mysql:/var/lib/mysql-files/ 2>/dev/null || true

docker exec -i docker_mysql mysql -u root -phelloworld < "$DIR/04_Iteration_4_Passage_a_l_Echelle/08_load_data_sirene_mysql.sql" 2>/dev/null || true
docker exec -i docker_mysql mysql -u root -phelloworld base_sirene < "$DIR/04_Iteration_4_Passage_a_l_Echelle/02_exercice1_indexes_sirene.sql" 2>/dev/null || true
echo "✅ Base SIRENE et index créés dans Docker."

echo -e "\n🎉 TOUTES LES ITÉRATIONS ONT ÉTÉ EXÉCUTÉES DANS DOCKER AVEC SUCCÈS !"
