#!/usr/bin/env bash
# =============================================================================
# SCRIPT D'IMPORTATION DE LA BASE SIRENE DANS DOCKER MYSQL (ITÉRATION 4)
# AVEC BARRE DE PROGRESSION EN TEMPS RÉEL
# =============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$DIR"

echo "=================================================="
echo "🐳 1. DÉMARRAGE DU CONTENEUR DOCKER MYSQL"
echo "=================================================="
docker compose up -d

echo -e "\n⏳ Attente du démarrage de MySQL..."
sleep 2

python3 "$DIR/04_Iteration_4_Passage_a_l_Echelle/import_with_progress.py"
