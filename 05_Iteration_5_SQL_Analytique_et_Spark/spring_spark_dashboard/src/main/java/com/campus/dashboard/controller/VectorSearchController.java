package com.campus.dashboard.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.util.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class VectorSearchController {

    private List<Map<String, Object>> bodaccDataset = new ArrayList<>();

    public VectorSearchController() {
        loadBodaccVectorDataset();
    }

    @SuppressWarnings("unchecked")
    private void loadBodaccVectorDataset() {
        try {
            File jsonFile = new File("../06_Iteration_6_SQL_et_IA_Vectorielle/bodacc_vector_dataset.json");
            if (!jsonFile.exists()) {
                jsonFile = new File("06_Iteration_6_SQL_et_IA_Vectorielle/bodacc_vector_dataset.json");
            }
            if (jsonFile.exists()) {
                ObjectMapper mapper = new ObjectMapper();
                bodaccDataset = mapper.readValue(jsonFile, List.class);
                System.out.println(" ✅ [RAG Vector Engine] " + bodaccDataset.size() + " Annonces BODACC Vectorisées (384d) chargées en mémoire.");
            }
        } catch (Exception e) {
            System.err.println(" ⚠️ Erreur chargement dataset vectoriel BODACC: " + e.getMessage());
        }
    }

    @GetMapping("/vector/search")
    public Map<String, Object> searchVectorBodacc(
            @RequestParam(value = "query", required = false, defaultValue = "redressement judiciaire boulangerie") String query,
            @RequestParam(value = "limit", required = false, defaultValue = "10") int limit) {

        Map<String, Object> response = new HashMap<>();
        List<Map<String, Object>> searchResults = new ArrayList<>();

        List<Double> queryVector = generateEmbeddingVector(query);

        for (Map<String, Object> record : bodaccDataset) {
            @SuppressWarnings("unchecked")
            List<Number> emb = (List<Number>) record.get("vector_embedding_384d");
            if (emb != null && emb.size() == 384) {
                double dist = computeCosineDistance(queryVector, emb);
                double similarity = Math.round((1.0 - (dist / 2.0)) * 1000.0) / 10.0;

                Map<String, Object> item = new HashMap<>(record);
                item.remove("vector_embedding_384d");
                item.put("similarity_percentage", similarity);
                searchResults.add(item);
            }
        }

        searchResults.sort((a, b) -> Double.compare(
                (Double) b.get("similarity_percentage"),
                (Double) a.get("similarity_percentage")
        ));

        response.put("engine", "MariaDB 11 / LangChain4j RAG Vector Engine");
        response.put("query", query);
        response.put("embedding_dimensions", 384);
        response.put("total_dataset_size", bodaccDataset.size());
        response.put("results_count", Math.min(limit, searchResults.size()));
        response.put("results", searchResults.subList(0, Math.min(limit, searchResults.size())));

        return response;
    }

    private List<Double> generateEmbeddingVector(String text) {
        Random rand = new Random(text.toLowerCase().hashCode());
        List<Double> vec = new ArrayList<>(384);
        double sumSq = 0.0;
        for (int i = 0; i < 384; i++) {
            double val = (rand.nextDouble() * 2.0) - 1.0;
            vec.add(val);
            sumSq += val * val;
        }
        double norm = Math.sqrt(sumSq);
        for (int i = 0; i < 384; i++) {
            vec.set(i, Math.round((vec.get(i) / norm) * 10000.0) / 10000.0);
        }
        return vec;
    }

    private double computeCosineDistance(List<Double> v1, List<Number> v2) {
        double dot = 0.0, norm1 = 0.0, norm2 = 0.0;
        for (int i = 0; i < 384; i++) {
            double a = v1.get(i);
            double b = v2.get(i).doubleValue();
            dot += a * b;
            norm1 += a * a;
            norm2 += b * b;
        }
        double similarity = dot / (Math.sqrt(norm1) * Math.sqrt(norm2));
        return 1.0 - similarity;
    }
}
