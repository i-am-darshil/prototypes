# Voice Search Query Intent Discovery via Clustering

## 1. Introduction

This report presents an end-to-end pipeline for discovering latent user intents from conversational voice search queries. Rather than relying on document retrieval, we focus on **query-side intelligence**: representing queries in vector space, clustering them to discover intent groups, and demonstrating how clustering improves retrieval and suggestion systems.

The pipeline processes 1,640 unique voice search queries across 8 languages and 5 intent categories, applying two representation methods (TF-IDF and multilingual sentence embeddings) and two clustering algorithms (K-Means and DBSCAN).

---

## 2. Dataset

### 2.1 Source

Took inspiration from a kaggle dataset which has a collection of 1,555 voice search queries. However, it contained only **25 unique English query texts** repeated many times, and the `language` column was inconsistent with the actual query text (e.g., English text labelled as "Spanish").

Kaggle dataset - https://www.kaggle.com/datasets/pratyushpuri/voice-search-1500-conversational-queries-2025

### 2.2 Dataset Regeneration

Since clustering requires diversity in the input data, we regenerated the dataset from scratch (`generate_queries.py`) with the following design:

**English queries** were generated programmatically using 30 templates per intent, each with multiple slot fillers (e.g., genres, place names, items, apps). This produced 2,369 unique English queries, from which 1,476 were sampled (balanced across intents) to hit the 90% target.

**Multilingual queries** were hand-curated: 24 queries each for Spanish, French, Hindi, Mandarin, German, and Japanese, plus 20 for Portuguese. These are genuine translations of voice search queries, not machine-translated.

### 2.3 Final Dataset Composition

| Language   | Unique Queries | Percentage |
|------------|---------------|------------|
| English    | 1,476         | 90.0%      |
| Spanish    | 24            | 1.5%       |
| French     | 24            | 1.5%       |
| Hindi      | 24            | 1.5%       |
| Mandarin   | 24            | 1.5%       |
| German     | 24            | 1.5%       |
| Japanese   | 24            | 1.5%       |
| Portuguese | 20            | 1.2%       |
| **Total**  | **1,640**     | **100%**   |

**Intent distribution:**

| Intent        | Count |
|---------------|-------|
| Shopping      | 402   |
| Navigation    | 391   |
| Information   | 329   |
| Command       | 273   |
| Entertainment | 245   |

### 2.4 Key Design Decisions

- **All 1,640 rows are unique** -- no duplicates. Duplicate queries add no information for clustering and artificially inflate cluster sizes.
- **Only `query_text`, `language`, and `intent` columns** are retained. Other metadata (device type, timestamp, confidence scores) are irrelevant for text clustering.
- The `intent` column serves as ground truth for **external validation only** -- it is not used during clustering.

---

## 3. Approach

### 3.1 Overview

The pipeline follows four stages:

```
Query Text --> Representation --> Clustering --> Evaluation
                                      |
                                      v
                              Query Suggestions
```

### 3.2 Query Representation

We implemented two representation methods:

#### 3.2.1 TF-IDF (Term Frequency--Inverse Document Frequency)

- **N-gram range:** unigrams + bigrams `(1, 2)`
- **Max features:** 5,000
- **Stop words:** English stop words removed
- **Min document frequency:** 2 (terms appearing in fewer than 2 documents are dropped)
- **Sublinear TF:** enabled (applies `1 + log(tf)` dampening)
- **Output:** sparse matrix of shape `(1640, 989)`

TF-IDF captures lexical patterns -- queries sharing the same keywords (e.g., "play", "navigate", "buy") will have similar vectors. However, it treats each language's tokens independently: "Play my favorite song" and "Joue ma chanson preferee" share zero features.

#### 3.2.2 Multilingual Sentence Embeddings

- **Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Embedding dimension:** 384
- **Languages supported:** 50+ (covers all 8 in our dataset)
- **Output:** dense matrix of shape `(1640, 384)`

This model maps semantically equivalent queries into nearby regions of a shared vector space, regardless of language. It captures meaning rather than surface form, making it suitable for cross-lingual clustering.

### 3.3 Clustering Algorithms

#### 3.3.1 K-Means

- **Hyperparameter sweep:** k = 3 to 10
- **Initialisation:** 10 restarts (`n_init=10`), best selected by inertia
- **Max iterations:** 300
- **Selection criterion:** highest silhouette score

K-Means is appropriate here because we have a prior expectation of ~5 intent groups, and the algorithm is efficient for moderate-sized datasets.

#### 3.3.2 DBSCAN (Density-Based Spatial Clustering)

- **Hyperparameter sweep:** eps = {0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0}
- **Min samples:** 5
- **Distance metric:** cosine
- **Selection criterion:** highest silhouette score (excluding noise points)

DBSCAN complements K-Means by discovering the number of clusters from data density and identifying outlier/noise queries. It does not require specifying k upfront.

### 3.4 Cross-Lingual Strategy

We use **shared multilingual embeddings** rather than translation-based normalisation. This avoids introducing a translation step (with its associated errors and API dependencies) and leverages the fact that the sentence-transformer model natively maps all languages into a common space.

### 3.5 Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **Silhouette Score** | Measures how similar a query is to its own cluster vs. nearest neighbouring cluster. Range: [-1, 1], higher is better. |
| **Cluster Purity** | Fraction of queries in each cluster belonging to the dominant intent. Range: [0, 1]. |
| **Normalised Mutual Information (NMI)** | Information-theoretic measure of agreement between clusters and true intents. Range: [0, 1]. |
| **Adjusted Rand Index (ARI)** | Chance-corrected measure of cluster-intent agreement. Range: [-1, 1], 0 = random. |
| **Cluster Stability** | Mean pairwise ARI across 10 K-Means runs with different random seeds. |
| **Cross-Lingual Language Entropy** | Normalised entropy of language distribution within each cluster. 1.0 = perfect mixing. |

---

## 4. Results

### 4.1 TF-IDF Clustering

#### K-Means Hyperparameter Sweep

| k  | Silhouette |
|----|-----------|
| 3  | 0.0206    |
| 4  | 0.0240    |
| 5  | 0.0304    |
| 6  | 0.0326    |
| 7  | 0.0387    |
| 8  | 0.0428    |
| 9  | **0.0549**|
| 10 | 0.0540    |

Best: **k=9** with silhouette 0.0549. The very low silhouette scores indicate poorly separated clusters -- TF-IDF struggles with the diverse vocabulary across 1,640 unique queries.

**Top terms for selected clusters (k=9):**

| Cluster | Top Terms | Interpretation |
|---------|-----------|----------------|
| 0 | turn, lights, door, timer | Device commands |
| 1 | route, fastest, scenic, best route | Route planning |
| 2 | order, online, replacement, delivery | Online shopping |
| 4 | open, app, google, spotify | App commands |
| 8 | buy, nearby, new, headphones | In-store shopping |

TF-IDF clusters around **surface-level verb patterns** ("turn", "open", "buy", "order") rather than semantic intent. This fragments navigation into separate "route", "drive", and "far" clusters.

#### DBSCAN Results

| eps | Clusters | Noise | Silhouette |
|-----|----------|-------|-----------|
| 0.3 | 60       | 1,219 | 0.7558    |
| 0.5 | 60       | 492   | 0.2015    |
| 0.7 | 7        | 154   | 0.0266    |
| 0.9 | 5        | 103   | 0.0255    |

DBSCAN with TF-IDF produces either too many micro-clusters (60 at eps=0.3, with 74% of data as noise) or collapses into very few clusters. The high silhouette at eps=0.3 is misleading -- it reflects tiny, pure clusters with most data unassigned.

**Stability:** Mean pairwise ARI = 0.3923 (moderate instability across runs).

### 4.2 Multilingual Embedding Clustering

#### K-Means Hyperparameter Sweep

| k  | Silhouette |
|----|-----------|
| 3  | 0.0804    |
| 4  | 0.0989    |
| 5  | 0.1132    |
| **6** | **0.1161** |
| 7  | 0.0942    |
| 8  | 0.0995    |
| 9  | 0.1045    |
| 10 | 0.1066    |

Best: **k=6** with silhouette 0.1161. While still modest in absolute terms (typical for high-dimensional semantic spaces), the relative improvement over TF-IDF is substantial.

**Cluster intent alignment (k=6):**

| Cluster | Dominant Intent | Purity | Size |
|---------|----------------|--------|------|
| 0 | Information     | 98.7%  | 236  |
| 1 | Navigation      | 94.1%  | 371  |
| 2 | Entertainment   | 88.2%  | 245  |
| 3 | Command         | 100.0% | 137  |
| 4 | Command (mixed) | 43.0%  | 272  |
| 5 | Shopping        | 92.1%  | 379  |

Five of six clusters align cleanly with ground-truth intents. Cluster 4 is a "catch-all" mixing commands, information queries, and some navigation -- these are short, action-oriented queries that are semantically close in embedding space (e.g., "Call Dad", "Set a reminder", "What time is it in Cairo?").

#### Cross-Lingual Cluster Composition

All 6 clusters contain queries from all 8 languages. For example, Cluster 1 (navigation) includes:
- English (339), Japanese (5), German (5), Spanish (5), Mandarin (5), Hindi (4), French (4), Portuguese (4)

This confirms that multilingual embeddings successfully map semantically equivalent queries across languages into the same clusters.

**Sample cross-lingual grouping (Cluster 1 -- Navigation):**
- "Navigate to the stadium" (English)
- "How far is Moscow from Berlin?" (English)
- "Directions to the convention center" (English)
- "सबसे नज़दीकी कॉफी शॉप ढूंढो" (Hindi)
- "Emmene-moi a l'aeroport" (French)
- "带我去机场" (Mandarin)

#### DBSCAN Results

| eps | Clusters | Noise | Silhouette |
|-----|----------|-------|-----------|
| 0.2 | 65       | 1,139 | 0.6601    |
| 0.3 | 67       | 653   | 0.2680    |
| 0.5 | 4        | 68    | 0.0307    |
| 0.6 | 1        | 8     | -1.0      |

DBSCAN with embeddings shows similar behaviour to TF-IDF: at low eps it creates many micro-clusters (sub-intent granularity), while at higher eps it collapses. The sweet spot (eps=0.5, 4 clusters) roughly aligns with broad intent groups but with significant noise.

**Stability:** Mean pairwise ARI = **0.8365** (highly stable across random initialisations).

### 4.3 Comparative Analysis

#### Best K-Means (Optimal k)

| Metric                       | TF-IDF | Embeddings |
|------------------------------|--------|------------|
| Best k                       | 9      | 6          |
| Silhouette                   | 0.0549 | 0.1161     |
| Purity                       | 0.3823 | 0.8543     |
| NMI                          | 0.2326 | 0.6871     |
| ARI                          | 0.0064 | 0.6746     |
| Stability (ARI, 10 runs)    | 0.3923 | 0.8365     |

#### At k=5 (Matching True Intent Count)

| Metric     | TF-IDF | Embeddings |
|------------|--------|------------|
| Silhouette | 0.0304 | 0.1132     |
| Purity     | 0.3299 | **0.9061** |
| NMI        | 0.1599 | **0.7458** |
| ARI        | 0.0138 | **0.7840** |

At k=5, embeddings achieve **90.6% purity** -- meaning 9 out of 10 queries are assigned to the correct intent cluster. TF-IDF manages only 33%.

#### Cross-Lingual Quality

| Metric                        | TF-IDF | Embeddings |
|-------------------------------|--------|------------|
| Mean normalised lang entropy  | 0.0460 | 0.2464     |

TF-IDF's near-zero entropy means multilingual queries are isolated in their own clusters (no cross-lingual mixing). Embeddings achieve meaningful mixing, though the score is below 1.0 because English dominates the dataset (90%).

### 4.4 Visualisation

Four plots were generated (PCA 2D projections):

- **`plot_tfidf_kmeans.png`** -- TF-IDF K-Means clusters vs true intents. Shows poorly separated, overlapping clusters.
- **`plot_embedding_kmeans.png`** -- Embedding K-Means clusters vs true intents. Shows cleaner separation with visible intent grouping.
- **`plot_embedding_dbscan.png`** -- Embedding DBSCAN clusters. Shows many small clusters with significant noise at eps=0.2.
- **`silhouette_comparison.png`** -- Side-by-side bar chart of silhouette scores across k values for both methods.

---

## 5. Query Suggestion and Retrieval Grouping

### 5.1 Cluster-Based Query Suggestions

We built a `ClusterBasedSuggester` that, given an input query:
1. Encodes the query using the multilingual embedding model
2. Identifies the nearest cluster centroid
3. Returns the top-k most similar queries within that cluster

**Selected results:**

**English input: "How do I get to the mall?"**

| Suggestion | Language | Similarity |
|------------|----------|-----------|
| How do I get to the mall? | English | 1.000 |
| Como llego al centro comercial? | Spanish | 0.980 |
| What's the best route to the mall? | English | 0.829 |
| Take me to the mall | English | 0.791 |
| How long to drive to the mall? | English | 0.741 |

The system correctly identifies the Spanish translation as the most similar alternative, then surfaces paraphrases of the same navigation intent.

**Japanese input: "最近のニュースを教えて" (Tell me recent news)**

| Suggestion | Language | Similarity |
|------------|----------|-----------|
| 今日のニュースの見出しを教えて | Japanese | 0.841 |
| Me diga as manchetes de hoje | Portuguese | 0.820 |
| Sag mir die Schlagzeilen | German | 0.806 |
| 告诉我今天的新闻头条 | Mandarin | 0.804 |
| Donne-moi les titres des actualites | French | 0.788 |

A Japanese query returns semantically equivalent news queries across 5 different languages -- all from the same intent cluster.

**German input: "Wie wird das Wetter morgen?" (How will the weather be tomorrow?)**

| Suggestion | Language | Similarity |
|------------|----------|-----------|
| 今日の天気はどう? | Japanese | 0.857 |
| 今天天气怎么样? | Mandarin | 0.842 |
| Quel temps fait-il aujourd'hui? | French | 0.842 |
| Wie ist das Wetter heute? | German | 0.839 |
| Como esta o tempo hoje? | Portuguese | 0.834 |

### 5.2 Retrieval Grouping

Clustering organises the 1,640 queries into 6 coherent groups. This enables:

1. **Intent-aware suggestions** -- constrain suggestions to the same intent cluster, avoiding cross-intent noise (e.g., "Play music" should not suggest "Buy headphones" even if they share the word "music")
2. **Multilingual query expansion** -- given a query in any language, find equivalent queries in all other languages
3. **Retrieval re-ranking** -- boost search results matching the query's cluster intent

---

## 6. Key Observations

1. **Multilingual embeddings vastly outperform TF-IDF** for intent clustering. At k=5, embeddings achieve 90.6% purity and 0.78 ARI vs TF-IDF's 33% purity and 0.01 ARI.

2. **TF-IDF clusters by verb pattern, not intent.** It separates "turn off the lights" from "set an alarm" (both commands) because they share no words, while grouping "open Spotify" with "open the calendar" based on the shared verb "open".

3. **Cross-lingual clustering works.** The multilingual embedding model maps "How do I get to the mall?" and "Como llego al centro comercial?" to nearly identical vectors (0.98 cosine similarity), enabling them to land in the same cluster without any translation step.

4. **K-Means is preferred over DBSCAN** for this task. DBSCAN either over-fragments into micro-clusters (eps=0.2: 65 clusters) or collapses (eps=0.6: 1 cluster). The semantic embedding space lacks the sharp density boundaries that DBSCAN requires.

5. **k=5 aligns with ground truth, but k=6 scores higher on silhouette.** The extra cluster splits "command" into device-control commands (turn on/off, timers) and communication commands (call, text, remind). This sub-intent split is semantically valid.

6. **Embedding clusters are highly stable** (ARI=0.84 across 10 random seeds), while TF-IDF clusters are unstable (ARI=0.39). This means embedding-based clusters are reproducible and trustworthy.

7. **Cluster 4 is a known weakness** at k=6: a mixed bag of short action-oriented queries from multiple intents (commands, weather, navigation) that are semantically close in embedding space. This suggests some intents have fuzzy boundaries that even semantic models struggle to separate.

---

## 7. Assumptions and Limitations

### Assumptions

- **Five latent intents exist** (entertainment, navigation, shopping, information, command). The dataset was generated with these labels, and we use them for external validation. In a real-world scenario, the "true" number of intents would be unknown.
- **Query text alone is sufficient** for intent clustering. In practice, context (user history, time of day, device type) would improve accuracy.
- **The multilingual embedding model generalises** to all 8 languages in the dataset. The model (`paraphrase-multilingual-MiniLM-L12-v2`) was trained on 50+ languages, so this is a reasonable assumption.

### Limitations

- **Synthetic data.** Template-generated queries are more uniform than real voice search logs. Real queries would exhibit more noise, misspellings, incomplete utterances, and ambiguity.
- **Imbalanced language distribution.** English dominates at 90%, making cross-lingual metrics less discriminating. A more balanced dataset would better stress-test multilingual clustering.
- **Low absolute silhouette scores.** Even the best configuration (embeddings, k=6) achieves only 0.116 silhouette. This is typical for high-dimensional semantic spaces where cluster boundaries are soft, but it means the clusters are not crisply separated.
- **DBSCAN underperforms.** The cosine distance distribution in sentence embedding space is relatively uniform, lacking the density gaps that DBSCAN exploits. Alternative density-based methods (HDBSCAN) may perform better.

---

## 8. Project Structure

```
search_query_intent_capture/
  generate_queries.py                          # Dataset generation (templates + multilingual)
  voice_search_query_captures_multilingual.csv # Final dataset (1,640 unique queries)
  data_loader.py                               # Shared data loading utility
  tfidf_clustering.py                          # TF-IDF representation + K-Means/DBSCAN
  embedding_clustering.py                      # Multilingual embeddings + K-Means/DBSCAN
  evaluation.py                                # Comparison metrics and visualisation
  query_suggestions.py                         # Cluster-based suggestion engine
  main.py                                      # Orchestrator (runs full pipeline)
  requirements.txt                             # Python dependencies
  plot_tfidf_kmeans.png                        # TF-IDF cluster visualisation
  plot_embedding_kmeans.png                    # Embedding cluster visualisation
  plot_embedding_dbscan.png                    # DBSCAN cluster visualisation
  silhouette_comparison.png                    # Silhouette score comparison chart
```

### Running the Pipeline

```bash
pyenv local 3.11.9
pip install -r requirements.txt

python3 main.py              # Full pipeline
python3 main.py --tfidf      # TF-IDF only
python3 main.py --embedding  # Embedding only
python3 main.py --suggest    # Query suggestion demo
```

### Dependencies

- Python 3.11
- pandas, numpy, scikit-learn
- sentence-transformers (for multilingual embeddings)
- matplotlib, seaborn (for visualisation)

---

## 9. Conclusion

Multilingual sentence embeddings combined with K-Means clustering effectively discover latent intent groups from voice search queries, achieving 90.6% purity at k=5 against ground-truth intents. The approach handles cross-lingual queries natively -- a Spanish shopping query clusters with its English equivalent without any translation step. TF-IDF serves as a useful baseline but fundamentally cannot bridge the vocabulary gap across languages or capture semantic similarity between syntactically different queries.

The cluster-based query suggestion system demonstrates practical value: given any query in any supported language, it returns semantically relevant suggestions from across all languages, constrained to the same intent group. This has direct applications in search auto-complete, query expansion, and intent-aware retrieval re-ranking.
