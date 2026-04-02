"""
Multilingual embedding-based query representation + clustering.

Uses sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 to map
all queries (across 7 languages) into a shared 384-dim vector space.

Pipeline:
  1. Encode queries with multilingual sentence embeddings
  2. Cluster with K-Means (sweep k=3..10)
  3. Cluster with DBSCAN (sweep eps)
  4. Evaluate with silhouette scores
  5. Analyse cross-lingual cluster composition
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, adjusted_rand_score
from collections import Counter

from data_loader import get_queries_and_labels

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# Representation
def build_embeddings(queries: list[str], model_name: str = MODEL_NAME) -> np.ndarray:
    """Encode queries into multilingual sentence embeddings."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(queries, show_progress_bar=True, batch_size=64)
    return embeddings


# Clustering
def run_kmeans(X: np.ndarray, k: int, random_state: int = 42) -> np.ndarray:
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10, max_iter=300)
    return km.fit_predict(X)


def run_dbscan(X: np.ndarray, eps: float, min_samples: int = 5) -> np.ndarray:
    db = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
    return db.fit_predict(X)


# Evaluation
def evaluate_silhouette(X: np.ndarray, labels: np.ndarray) -> float:
    unique = set(labels)
    unique.discard(-1)
    if len(unique) < 2:
        return -1.0
    mask = labels != -1
    if mask.sum() < 2:
        return -1.0
    return silhouette_score(X[mask], labels[mask], metric="cosine")


def sweep_kmeans(X: np.ndarray, k_range: range = range(3, 11)) -> dict:
    results = {}
    for k in k_range:
        labels = run_kmeans(X, k)
        sil = evaluate_silhouette(X, labels)
        results[k] = {"labels": labels, "silhouette": sil}
        print(f"  K-Means k={k}: silhouette={sil:.4f}")
    return results


def sweep_dbscan(X: np.ndarray, eps_values: list[float] = None, min_samples: int = 5) -> dict:
    if eps_values is None:
        eps_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
    results = {}
    for eps in eps_values:
        labels = run_dbscan(X, eps, min_samples)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = (labels == -1).sum()
        sil = evaluate_silhouette(X, labels)
        results[eps] = {"labels": labels, "silhouette": sil, "n_clusters": n_clusters, "n_noise": n_noise}
        print(f"  DBSCAN eps={eps}: clusters={n_clusters}, noise={n_noise}, silhouette={sil:.4f}")
    return results


# Cluster stability
def assess_kmeans_stability(X: np.ndarray, k: int, n_runs: int = 10) -> float:
    all_labels = []
    for i in range(n_runs):
        labels = run_kmeans(X, k, random_state=i * 7 + 1)
        all_labels.append(labels)

    ari_scores = []
    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            ari_scores.append(adjusted_rand_score(all_labels[i], all_labels[j]))
    return np.mean(ari_scores)


# Cross-lingual analysis
def analyse_cross_lingual(df: pd.DataFrame, labels: np.ndarray, k: int):
    """Show language distribution within each cluster."""
    df = df.copy()
    df["cluster"] = labels

    print(f"\n  Language distribution per cluster (K-Means k={k}):")
    for cid in range(k):
        cluster_df = df[df["cluster"] == cid]
        lang_counts = cluster_df["language"].value_counts().to_dict()
        intent_counts = cluster_df["intent"].value_counts().to_dict()
        dominant_intent = max(intent_counts, key=intent_counts.get)
        total = len(cluster_df)
        lang_str = ", ".join(f"{l}:{c}" for l, c in sorted(lang_counts.items(), key=lambda x: -x[1]))
        print(f"  Cluster {cid} (n={total}, dominant_intent={dominant_intent}): {lang_str}")


def analyse_intent_alignment(df: pd.DataFrame, labels: np.ndarray):
    """Show how clusters align with true intents."""
    df = df.copy()
    df["cluster"] = labels

    print("\n  Cluster → Intent mapping:")
    for cid in sorted(df["cluster"].unique()):
        if cid == -1:
            continue
        cluster_df = df[df["cluster"] == cid]
        intent_counts = cluster_df["intent"].value_counts()
        dominant = intent_counts.index[0]
        purity = intent_counts.iloc[0] / len(cluster_df)
        print(f"  Cluster {cid}: {dominant} ({purity:.1%} purity, n={len(cluster_df)})")


# Frequent intent pattern extraction
def extract_intent_patterns(df: pd.DataFrame, labels: np.ndarray):
    """Extract frequent query patterns per cluster."""
    df = df.copy()
    df["cluster"] = labels

    print("\n  Frequent query patterns per cluster:")
    for cid in sorted(df["cluster"].unique()):
        if cid == -1:
            continue
        cluster_df = df[df["cluster"] == cid]
        query_counts = cluster_df["query_text"].value_counts().head(5)
        print(f"  Cluster {cid}:")
        for query, count in query_counts.items():
            print(f"    \"{query}\" (x{count})")


def run_embedding_pipeline() -> dict:
    """Run the full multilingual embedding clustering pipeline."""
    print("=" * 60)
    print("MULTILINGUAL EMBEDDING CLUSTERING PIPELINE")
    print("=" * 60)

    # Load data
    df, queries, intents = get_queries_and_labels()
    print(f"\nLoaded {len(queries)} queries across {df['language'].nunique()} languages")

    # Build embeddings
    print(f"\n── Encoding queries with {MODEL_NAME} ──")
    X = build_embeddings(queries)
    print(f"Embedding shape: {X.shape}")

    # K-Means sweep
    print("\n── K-Means hyperparameter sweep ──")
    kmeans_results = sweep_kmeans(X)

    best_k = max(kmeans_results, key=lambda k: kmeans_results[k]["silhouette"])
    best_km = kmeans_results[best_k]
    print(f"\n  Best k={best_k} (silhouette={best_km['silhouette']:.4f})")

    # DBSCAN sweep
    print("\n── DBSCAN hyperparameter sweep ──")
    dbscan_results = sweep_dbscan(X)

    valid_dbscan = {e: r for e, r in dbscan_results.items() if r["silhouette"] > 0}
    if valid_dbscan:
        best_eps = max(valid_dbscan, key=lambda e: valid_dbscan[e]["silhouette"])
        best_db = dbscan_results[best_eps]
        print(f"\n  Best eps={best_eps} (silhouette={best_db['silhouette']:.4f}, clusters={best_db['n_clusters']})")
    else:
        best_eps = None
        best_db = None
        print("\n  No valid DBSCAN configuration found.")

    # Cross-lingual analysis
    print("\n── Cross-lingual cluster analysis ──")
    analyse_cross_lingual(df, best_km["labels"], best_k)

    # Intent alignment
    print("\n── Intent alignment ──")
    analyse_intent_alignment(df, best_km["labels"])

    # Frequent patterns
    print("\n── Frequent intent patterns ──")
    extract_intent_patterns(df, best_km["labels"])

    # Stability
    print(f"\n── K-Means stability (k={best_k}, 10 runs) ──")
    stability = assess_kmeans_stability(X, best_k)
    print(f"  Mean pairwise ARI: {stability:.4f}")

    return {
        "X": X,
        "queries": queries,
        "intents": intents,
        "df": df,
        "kmeans_results": kmeans_results,
        "best_k": best_k,
        "dbscan_results": dbscan_results,
        "best_eps": best_eps,
        "stability": stability,
    }


if __name__ == "__main__":
    run_embedding_pipeline()
