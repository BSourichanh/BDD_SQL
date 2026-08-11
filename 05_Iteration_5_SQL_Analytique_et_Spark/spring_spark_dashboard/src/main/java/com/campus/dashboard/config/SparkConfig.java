package com.campus.dashboard.config;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;
import java.io.File;

@Configuration
public class SparkConfig {

    private SparkSession sparkSession;
    private Dataset<Row> sireneParquetDataset;

    @PostConstruct
    public void initSparkSession() {
        System.out.println("==========================================================");
        System.out.println(" 🚀 INITIALISATION DE LA SPARK SESSION IN-MEMORY (SPRING BOOT)");
        System.out.println("==========================================================");

        this.sparkSession = SparkSession.builder()
                .appName("SpringSparkAnalyticsDashboard")
                .master("local[*]")
                .config("spark.sql.shuffle.partitions", "4")
                .getOrCreate();

        String parquetPath = "../sirene_analytique_commune.csv";
        File f = new File(parquetPath);
        if (!f.exists()) {
            parquetPath = "05_Iteration_5_SQL_Analytique_et_Spark/sirene_analytique_commune.csv";
        }

        System.out.println(" 📖 Chargement In-Memory du Dataset Parquet/CSV : " + parquetPath);
        this.sireneParquetDataset = this.sparkSession.read()
                .option("header", "true")
                .option("inferSchema", "true")
                .csv(parquetPath)
                .cache();

        this.sireneParquetDataset.createOrReplaceTempView("sirene_communes");
        System.out.println(" ✅ DATASET SPARK EN MÉMOIRE RAM PRETS POUR LES REQUÊTES EN " + this.sireneParquetDataset.count() + " LIGNES !");
        System.out.println("==========================================================");
    }

    @Bean
    public SparkSession getSparkSession() {
        return this.sparkSession;
    }

    @Bean
    public Dataset<Row> getSireneParquetDataset() {
        return this.sireneParquetDataset;
    }
}
