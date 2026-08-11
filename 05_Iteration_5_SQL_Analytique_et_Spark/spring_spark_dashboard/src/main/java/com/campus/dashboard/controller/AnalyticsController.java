package com.campus.dashboard.controller;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AnalyticsController {

    @Autowired
    private SparkSession sparkSession;

    @Autowired
    private Dataset<Row> sireneParquetDataset;

    @GetMapping("/analytics")
    public Map<String, Object> getAnalyticsData() {
        Map<String, Object> response = new HashMap<>();

        // Requête Spark SQL In-Memory sur les Datasets
        Dataset<Row> topCommunes = sparkSession.sql(
                "SELECT commune, code_postal, departement, nb_etablissements " +
                "FROM sirene_communes ORDER BY nb_etablissements DESC LIMIT 10"
        );

        List<Row> rows = topCommunes.collectAsList();

        response.put("engine", "Apache Spark + Spring Boot Java Engine");
        response.put("total_communes", sireneParquetDataset.count());
        response.put("top_10_communes_sample", rows.toString());

        return response;
    }
}
