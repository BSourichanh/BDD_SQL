package com.campus.dashboard;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import java.io.File;

public class ConvertTotaleToParquet {
    public static void main(String[] args) {
        System.out.println("==========================================================================");
        System.out.println(" 🚀 CONVERSION SPARK DE LA BASE TOTALE CSV EN PARQUET BINAIRE (3.5 GB)");
        System.out.println("==========================================================================");

        SparkSession spark = SparkSession.builder()
                .appName("CsvToParquetConverter")
                .master("local[*]")
                .config("spark.sql.shuffle.partitions", "4")
                .getOrCreate();

        String csvPath = "../sirene_analytique_totale.csv";
        if (!new File(csvPath).exists()) {
            csvPath = "05_Iteration_5_SQL_Analytique_et_Spark/sirene_analytique_totale.csv";
        }

        String parquetPath = csvPath.replace(".csv", ".parquet");

        System.out.println(" 📖 Lecture Spark de : " + csvPath);
        Dataset<Row> df = spark.read()
                .option("header", "true")
                .option("inferSchema", "true")
                .csv(csvPath);

        System.out.println(" 💾 Écriture du fichier binaire Parquet : " + parquetPath);
        df.write().mode("overwrite").parquet(parquetPath);

        System.out.println("==========================================================================");
        System.out.println(" ✅ FICHIER PARQUET TOTALE CRÉÉ AVEC SUCCÈS : " + parquetPath);
        System.out.println("==========================================================================");
        spark.stop();
    }
}
