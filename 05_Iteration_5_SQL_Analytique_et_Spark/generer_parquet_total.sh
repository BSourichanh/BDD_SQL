#!/usr/bin/env bash
# =============================================================================
# SCRIPT DE GÉNÉRATION DU PARQUET BINAIRE DE LA BASE TOTALE (3.5 GB)
# =============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================================================="
echo " 🚀 GÉNÉRATION DU PARQUET BINAIRE DE LA BASE TOTALE (43.8M ÉTABLISSEMENTS)"
echo "=========================================================================="
echo " 📖 Source CSV : $DIR/sirene_analytique_totale.csv (3.67 Go)"
echo " 💾 Cible PARQUET : $DIR/sirene_analytique_totale.parquet"
echo "=========================================================================="

# Supprimer tout fichier/dossier 0 octet résiduel
rm -rf "$DIR/sirene_analytique_totale.parquet"

sudo docker run --rm -v "$DIR:/data" python:3.12-slim bash -c "pip install duckdb && python3 -c \"import duckdb; duckdb.sql('COPY (SELECT * FROM read_csv_auto(\\\"/data/sirene_analytique_totale.csv\\\")) TO \\\"/data/sirene_analytique_totale.parquet\\\" (FORMAT PARQUET)')\""

echo -e "\n✅ LE DOSSIER/FICHIER PARQUET TOTALE A ÉTÉ GÉNÉRÉ AVEC SUCCÈS !"
ls -lh "$DIR/sirene_analytique_totale.parquet"
