### Query Representation — TF-IDF + Multilingual Embeddings

  TF-IDF — Good baseline. Simple, interpretable, and works well for discovering surface-level patterns (e.g., "nearest", "play", "buy" as intent signals). However, it treats each language's tokens as separate features, so it won't cluster "Pon mi canción favorita" with
  "Play my favorite song".

  Multilingual Embeddings — This is where the real value is. A model like sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 maps all 7 languages into a shared vector space. "Play my favorite song" and "播放我喜欢的歌" would land near each other. This directly
  solves cross-lingual clustering.

  Skip N-gram vectors — They'd add bulk without much insight beyond what TF-IDF already gives for short queries like these (avg 3-6 words).

### Cross-Lingual Strategy — Shared Multilingual Embeddings

  - Translation adds a fragile pipeline step (translation errors propagate)
  - Multilingual sentence-transformers handle this natively — one model, no translation API needed
  - We already need embeddings for representation, so this covers two requirements at once

  We'll run TF-IDF clustering as a monolingual baseline, then show how multilingual embeddings improve cross-lingual grouping — a clean comparison.

### Clustering Algorithms — K-Means + DBSCAN

  K-Means — We also sweep k=3..10 to test stability and find the "natural" cluster count via silhouette scores.

  DBSCAN — Complements K-Means well because:
  - It doesn't require specifying k upfront — it discovers cluster count from data density
  - It identifies outliers/noise (useful for ambiguous queries)
  - Interesting to compare: does DBSCAN find the same 5 groups, or does it discover sub-intents?

### Summary
```
  ┌──────────────────┬─────────────────────────────────────┬────────────────────────────────────────────────────────────────┐
  │     Decision     │               Choice                │                           Rationale                            │
  ├──────────────────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ Representation 1 │ TF-IDF                              │ Interpretable baseline, top-term extraction for cluster labels │
  ├──────────────────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ Representation 2 │ Multilingual sentence embeddings    │ Cross-lingual support, semantic similarity                     │
  ├──────────────────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ Cross-lingual    │ Shared embeddings (not translation) │ Simpler, no external API, one model                            │
  ├──────────────────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ Clustering 1     │ K-Means                             │ Known k=5, hyperparameter sweep                                │
  ├──────────────────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ Clustering 2     │ DBSCAN                              │ Discovers k, finds outliers, density-based contrast            │
  └──────────────────┴─────────────────────────────────────┴────────────────────────────────────────────────────────────────┘
```

### Setup
```bash
python3 -m pip install --index-url https://pypi.org/simple/ -r requirements.txt
```

### Project Setup
```
  search_query_intent_capture/
  ├── requirements.txt                              # Dependencies
  ├── data_loader.py                                # Shared CSV loading + query extraction
  ├── tfidf_clustering.py                           # TF-IDF representation + K-Means/DBSCAN
  ├── embedding_clustering.py                       # Multilingual embeddings + K-Means/DBSCAN
  ├── evaluation.py                                 # Comparison, metrics, plots
  ├── query_suggestions.py                          # Cluster-based suggestions + retrieval grouping
  ├── main.py                                       # Orchestrator (runs all pipelines)
  ├── generate_queries.py                           # Multilingual data generation
  ├── voice_search_query_captures_multilingual.csv  # Dataset
  ├── plot_tfidf_kmeans.png                         # TF-IDF cluster visualization
  ├── plot_embedding_kmeans.png                     # Embedding cluster visualization
  ├── plot_embedding_dbscan.png                     # DBSCAN cluster visualization
  └── silhouette_comparison.png                     # Silhouette score comparison chart
```

### Dataset
```
Total: 1640 unique queries
Intents: {'shopping': 402, 'navigation': 391, 'information': 329, 'command': 273, 'entertainment': 245}
Languages: {'English': 1476, 'Hindi': 24, 'German': 24, 'French': 24, 'Japanese': 24, 'Mandarin': 24, 'Spanish': 24, 'Portuguese': 20}
```

### Run
```bash
python3 main.py              # Full pipeline
python3 main.py --tfidf      # TF-IDF only
python3 main.py --embedding  # Embedding only
python3 main.py --suggest    # Suggestion demo
```