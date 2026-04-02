"""
TF-IDF based query representation + clustering.

Pipeline:
  1. Vectorize queries using TF-IDF (unigram + bigram)
  2. Cluster with K-Means (sweep k=3..10)
  3. Cluster with DBSCAN (sweep eps)
  4. Evaluate with silhouette scores
  5. Extract top terms per cluster for labelling
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

from data_loader import get_queries_and_labels


# Representation
def build_tfidf_matrix(queries: list[str]) -> tuple[TfidfVectorizer, np.ndarray]:
    """Build TF-IDF matrix with unigrams and bigrams."""
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words="english",
        min_df=2,
        sublinear_tf=True,
    )
    X = vectorizer.fit_transform(queries)
    return vectorizer, X


# Clustering
def run_kmeans(X, k: int, random_state: int = 42) -> np.ndarray:
    """Run K-Means and return cluster labels."""
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10, max_iter=300)
    return km.fit_predict(X)


def run_dbscan(X, eps: float, min_samples: int = 5) -> np.ndarray:
    """Run DBSCAN and return cluster labels (-1 = noise)."""
    db = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
    return db.fit_predict(X)


# ── Evaluation ──────────────────────────────────────────────────────────────

def evaluate_silhouette(X, labels: np.ndarray) -> float:
    """Compute silhouette score. Returns -1 if clustering is degenerate."""
    unique = set(labels)
    unique.discard(-1)
    if len(unique) < 2:
        return -1.0
    # Filter out noise points for silhouette
    mask = labels != -1
    if mask.sum() < 2:
        return -1.0
    return silhouette_score(X[mask], labels[mask], metric="cosine")


def sweep_kmeans(X, k_range: range = range(3, 11)) -> dict:
    """Sweep K-Means over k values, return {k: (labels, silhouette)}."""
    results = {}
    for k in k_range:
        labels = run_kmeans(X, k)
        sil = evaluate_silhouette(X, labels)
        results[k] = {"labels": labels, "silhouette": sil}
        print(f"  K-Means k={k}: silhouette={sil:.4f}")
    return results


def sweep_dbscan(X, eps_values: list[float] = None, min_samples: int = 5) -> dict:
    """Sweep DBSCAN over eps values."""
    if eps_values is None:
        eps_values = [0.3, 0.5, 0.7, 0.9, 1.0, 1.2, 1.5]
    results = {}
    for eps in eps_values:
        labels = run_dbscan(X, eps, min_samples)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = (labels == -1).sum()
        sil = evaluate_silhouette(X, labels)
        results[eps] = {"labels": labels, "silhouette": sil, "n_clusters": n_clusters, "n_noise": n_noise}
        print(f"  DBSCAN eps={eps}: clusters={n_clusters}, noise={n_noise}, silhouette={sil:.4f}")
    return results


# ── Cluster labelling ───────────────────────────────────────────────────────

def get_top_terms_per_cluster(vectorizer: TfidfVectorizer, X, labels: np.ndarray, n_terms: int = 10) -> dict:
    """Extract top TF-IDF terms per cluster for labelling."""
    feature_names = vectorizer.get_feature_names_out()
    cluster_terms = {}
    for cid in sorted(set(labels)):
        if cid == -1:
            continue
        mask = labels == cid
        centroid = X[mask].mean(axis=0)
        centroid = np.asarray(centroid).flatten()
        top_indices = centroid.argsort()[::-1][:n_terms]
        terms = [(feature_names[i], centroid[i]) for i in top_indices]
        cluster_terms[cid] = terms
    return cluster_terms


def print_cluster_labels(cluster_terms: dict):
    """Pretty-print top terms for each cluster."""
    for cid, terms in cluster_terms.items():
        term_str = ", ".join(f"{t}({w:.3f})" for t, w in terms)
        print(f"  Cluster {cid}: {term_str}")


# ── Cluster stability ──────────────────────────────────────────────────────

def assess_kmeans_stability(X, k: int, n_runs: int = 10) -> float:
    """
    Run K-Means n_runs times with different seeds.
    Return mean pairwise Adjusted Rand Index between runs as stability measure.
    """
    from sklearn.metrics import adjusted_rand_score
    all_labels = []
    for i in range(n_runs):
        labels = run_kmeans(X, k, random_state=i * 7 + 1)
        all_labels.append(labels)

    ari_scores = []
    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            ari_scores.append(adjusted_rand_score(all_labels[i], all_labels[j]))
    return np.mean(ari_scores)


# ── Main ────────────────────────────────────────────────────────────────────

def run_tfidf_pipeline() -> dict:
    """Run the full TF-IDF clustering pipeline. Returns results dict."""
    print("=" * 60)
    print("TF-IDF CLUSTERING PIPELINE")
    print("=" * 60)

    # Load data
    df, queries, intents = get_queries_and_labels()
    print(f"\nLoaded {len(queries)} queries")

    # Build TF-IDF
    print("\n── Building TF-IDF matrix ──")
    vectorizer, X = build_tfidf_matrix(queries)
    print(f"TF-IDF shape: {X.shape}")

    # K-Means sweep
    print("\n── K-Means hyperparameter sweep ──")
    kmeans_results = sweep_kmeans(X)

    # Best K-Means
    best_k = max(kmeans_results, key=lambda k: kmeans_results[k]["silhouette"])
    best_km = kmeans_results[best_k]
    print(f"\n  Best k={best_k} (silhouette={best_km['silhouette']:.4f})")

    # Cluster labels for best K-Means
    print(f"\n── Top terms per cluster (K-Means k={best_k}) ──")
    cluster_terms = get_top_terms_per_cluster(vectorizer, X, best_km["labels"])
    print_cluster_labels(cluster_terms)

    # DBSCAN sweep
    print("\n── DBSCAN hyperparameter sweep ──")
    dbscan_results = sweep_dbscan(X)

    # Best DBSCAN
    valid_dbscan = {e: r for e, r in dbscan_results.items() if r["silhouette"] > 0}
    if valid_dbscan:
        best_eps = max(valid_dbscan, key=lambda e: valid_dbscan[e]["silhouette"])
        best_db = dbscan_results[best_eps]
        print(f"\n  Best eps={best_eps} (silhouette={best_db['silhouette']:.4f}, clusters={best_db['n_clusters']})")

        print(f"\n── Top terms per cluster (DBSCAN eps={best_eps}) ──")
        db_cluster_terms = get_top_terms_per_cluster(vectorizer, X, best_db["labels"])
        print_cluster_labels(db_cluster_terms)
    else:
        best_eps = None
        best_db = None
        print("\n  No valid DBSCAN configuration found.")

    # Stability analysis for best K-Means
    print(f"\n── K-Means stability (k={best_k}, 10 runs) ──")
    stability = assess_kmeans_stability(X, best_k)
    print(f"  Mean pairwise ARI: {stability:.4f}")

    # Cross-lingual note
    print("\n── Cross-lingual note ──")
    print("  TF-IDF treats each language's tokens independently.")
    print("  Multilingual queries will NOT cluster with English equivalents.")
    print("  See embedding_clustering.py for cross-lingual clustering.")

    return {
        "vectorizer": vectorizer,
        "X": X,
        "queries": queries,
        "intents": intents,
        "df": df,
        "kmeans_results": kmeans_results,
        "best_k": best_k,
        "dbscan_results": dbscan_results,
        "best_eps": best_eps,
        "cluster_terms": cluster_terms,
        "stability": stability,
    }


if __name__ == "__main__":
    run_tfidf_pipeline()
