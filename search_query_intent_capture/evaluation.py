"""
Evaluation and comparison module.

Compares TF-IDF vs multilingual embeddings across:
  - Silhouette scores (K-Means and DBSCAN)
  - Cluster purity against true intents
  - Cross-lingual clustering quality
  - Cluster stability
  - Visualisation (PCA 2D projections)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score, adjusted_rand_score, normalized_mutual_info_score
from sklearn.decomposition import PCA
from collections import Counter

from data_loader import get_queries_and_labels


# Metrics
def cluster_purity(true_labels: list[str], cluster_labels: np.ndarray) -> float:
    """
    Purity: fraction of samples in each cluster that belong to the dominant class.
    Higher is better (1.0 = perfect).
    """
    total = 0
    correct = 0
    for cid in set(cluster_labels):
        if cid == -1:
            continue
        mask = cluster_labels == cid
        cluster_true = [true_labels[i] for i in range(len(true_labels)) if mask[i]]
        counts = Counter(cluster_true)
        correct += counts.most_common(1)[0][1]
        total += len(cluster_true)
    return correct / total if total > 0 else 0.0


def compute_nmi(true_labels: list[str], cluster_labels: np.ndarray) -> float:
    """Normalized Mutual Information between true intents and clusters."""
    mask = cluster_labels != -1
    if mask.sum() < 2:
        return 0.0
    filtered_true = [true_labels[i] for i in range(len(true_labels)) if mask[i]]
    return normalized_mutual_info_score(filtered_true, cluster_labels[mask])


def compute_ari(true_labels: list[str], cluster_labels: np.ndarray) -> float:
    """Adjusted Rand Index between true intents and clusters."""
    mask = cluster_labels != -1
    if mask.sum() < 2:
        return 0.0
    filtered_true = [true_labels[i] for i in range(len(true_labels)) if mask[i]]
    return adjusted_rand_score(filtered_true, cluster_labels[mask])


# Cross-lingual quality
def cross_lingual_score(df: pd.DataFrame, labels: np.ndarray) -> dict:
    """
    Measure how well multilingual queries cluster with their semantic equivalents.
    For each cluster, compute language entropy — uniform distribution = good cross-lingual mixing.
    """
    from scipy.stats import entropy

    df = df.copy()
    df["cluster"] = labels
    languages = df["language"].unique()
    n_languages = len(languages)

    cluster_entropies = {}
    for cid in sorted(set(labels)):
        if cid == -1:
            continue
        cluster_df = df[df["cluster"] == cid]
        lang_counts = cluster_df["language"].value_counts()
        proportions = lang_counts.values / lang_counts.values.sum()
        h = entropy(proportions, base=2)
        max_h = np.log2(min(n_languages, len(lang_counts)))
        normalized_h = h / max_h if max_h > 0 else 0
        cluster_entropies[cid] = {
            "entropy": h,
            "normalized_entropy": normalized_h,
            "n_languages": len(lang_counts),
            "size": len(cluster_df),
        }

    mean_normalized = np.mean([v["normalized_entropy"] for v in cluster_entropies.values()])
    return {"per_cluster": cluster_entropies, "mean_normalized_entropy": mean_normalized}


# Comparison
def compare_approaches(tfidf_results: dict, emb_results: dict):
    """Print a side-by-side comparison of TF-IDF vs embedding clustering."""
    _, _, intents = get_queries_and_labels()

    print("=" * 60)
    print("COMPARISON: TF-IDF vs MULTILINGUAL EMBEDDINGS")
    print("=" * 60)

    # Best K-Means
    tfidf_k = tfidf_results["best_k"]
    emb_k = emb_results["best_k"]
    tfidf_labels = tfidf_results["kmeans_results"][tfidf_k]["labels"]
    emb_labels = emb_results["kmeans_results"][emb_k]["labels"]

    tfidf_sil = tfidf_results["kmeans_results"][tfidf_k]["silhouette"]
    emb_sil = emb_results["kmeans_results"][emb_k]["silhouette"]

    print(f"\n── Best K-Means ──")
    print(f"  {'Metric':<30} {'TF-IDF':>12} {'Embeddings':>12}")
    print(f"  {'-'*54}")
    print(f"  {'Best k':<30} {tfidf_k:>12} {emb_k:>12}")
    print(f"  {'Silhouette':<30} {tfidf_sil:>12.4f} {emb_sil:>12.4f}")
    print(f"  {'Purity':<30} {cluster_purity(intents, tfidf_labels):>12.4f} {cluster_purity(intents, emb_labels):>12.4f}")
    print(f"  {'NMI':<30} {compute_nmi(intents, tfidf_labels):>12.4f} {compute_nmi(intents, emb_labels):>12.4f}")
    print(f"  {'ARI':<30} {compute_ari(intents, tfidf_labels):>12.4f} {compute_ari(intents, emb_labels):>12.4f}")
    print(f"  {'Stability (ARI, 10 runs)':<30} {tfidf_results['stability']:>12.4f} {emb_results['stability']:>12.4f}")

    # Compare at k=5 (matching true intent count)
    print(f"\n── At k=5 (true intent count) ──")
    if 5 in tfidf_results["kmeans_results"] and 5 in emb_results["kmeans_results"]:
        t5 = tfidf_results["kmeans_results"][5]
        e5 = emb_results["kmeans_results"][5]
        print(f"  {'Metric':<30} {'TF-IDF':>12} {'Embeddings':>12}")
        print(f"  {'-'*54}")
        print(f"  {'Silhouette':<30} {t5['silhouette']:>12.4f} {e5['silhouette']:>12.4f}")
        print(f"  {'Purity':<30} {cluster_purity(intents, t5['labels']):>12.4f} {cluster_purity(intents, e5['labels']):>12.4f}")
        print(f"  {'NMI':<30} {compute_nmi(intents, t5['labels']):>12.4f} {compute_nmi(intents, e5['labels']):>12.4f}")
        print(f"  {'ARI':<30} {compute_ari(intents, t5['labels']):>12.4f} {compute_ari(intents, e5['labels']):>12.4f}")

    # Cross-lingual
    print(f"\n── Cross-lingual clustering quality (best K-Means) ──")
    df = tfidf_results["df"]
    tfidf_xl = cross_lingual_score(df, tfidf_labels)
    emb_xl = cross_lingual_score(df, emb_labels)
    print(f"  {'Metric':<30} {'TF-IDF':>12} {'Embeddings':>12}")
    print(f"  {'-'*54}")
    print(f"  {'Mean normalized lang entropy':<30} {tfidf_xl['mean_normalized_entropy']:>12.4f} {emb_xl['mean_normalized_entropy']:>12.4f}")
    print(f"  (1.0 = perfect language mixing across clusters)")


# Visualisation
def plot_clusters_pca(X, labels: np.ndarray, title: str, filename: str, intents: list[str] = None):
    """2D PCA scatter plot of clusters."""
    if hasattr(X, "toarray"):
        X_dense = X.toarray()
    else:
        X_dense = X

    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_dense)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot by cluster
    ax = axes[0]
    unique_labels = sorted(set(labels))
    for cid in unique_labels:
        mask = labels == cid
        label = f"Noise" if cid == -1 else f"Cluster {cid}"
        alpha = 0.3 if cid == -1 else 0.6
        ax.scatter(coords[mask, 0], coords[mask, 1], s=10, alpha=alpha, label=label)
    ax.set_title(f"{title} — by cluster")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    if len(unique_labels) <= 12:
        ax.legend(fontsize=7, markerscale=2)

    # Plot by true intent
    if intents:
        ax = axes[1]
        intent_set = sorted(set(intents))
        colors = sns.color_palette("husl", len(intent_set))
        for idx, intent in enumerate(intent_set):
            mask = np.array([i == intent for i in intents])
            ax.scatter(coords[mask, 0], coords[mask, 1], s=10, alpha=0.6, label=intent, color=colors[idx])
        ax.set_title(f"{title} — by true intent")
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
        ax.legend(fontsize=8, markerscale=2)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filename}")


def plot_silhouette_comparison(tfidf_results: dict, emb_results: dict, filename: str = "silhouette_comparison.png"):
    """Bar chart comparing silhouette scores across k values."""
    k_range = sorted(set(tfidf_results["kmeans_results"].keys()) & set(emb_results["kmeans_results"].keys()))

    tfidf_sils = [tfidf_results["kmeans_results"][k]["silhouette"] for k in k_range]
    emb_sils = [emb_results["kmeans_results"][k]["silhouette"] for k in k_range]

    x = np.arange(len(k_range))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width / 2, tfidf_sils, width, label="TF-IDF", color="steelblue")
    ax.bar(x + width / 2, emb_sils, width, label="Multilingual Embeddings", color="coral")
    ax.set_xlabel("k (number of clusters)")
    ax.set_ylabel("Silhouette Score")
    ax.set_title("K-Means Silhouette Score: TF-IDF vs Multilingual Embeddings")
    ax.set_xticks(x)
    ax.set_xticklabels(k_range)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filename}")


def generate_all_plots(tfidf_results: dict, emb_results: dict):
    """Generate all visualisation plots."""
    print("\n── Generating plots ──")

    intents = tfidf_results["intents"]

    # TF-IDF best K-Means
    tfidf_k = tfidf_results["best_k"]
    plot_clusters_pca(
        tfidf_results["X"],
        tfidf_results["kmeans_results"][tfidf_k]["labels"],
        f"TF-IDF K-Means (k={tfidf_k})",
        "plot_tfidf_kmeans.png",
        intents,
    )

    # Embedding best K-Means
    emb_k = emb_results["best_k"]
    plot_clusters_pca(
        emb_results["X"],
        emb_results["kmeans_results"][emb_k]["labels"],
        f"Embedding K-Means (k={emb_k})",
        "plot_embedding_kmeans.png",
        intents,
    )

    # Embedding DBSCAN
    if emb_results["best_eps"] is not None:
        best_eps = emb_results["best_eps"]
        plot_clusters_pca(
            emb_results["X"],
            emb_results["dbscan_results"][best_eps]["labels"],
            f"Embedding DBSCAN (eps={best_eps})",
            "plot_embedding_dbscan.png",
            intents,
        )

    # Silhouette comparison
    plot_silhouette_comparison(tfidf_results, emb_results)


if __name__ == "__main__":
    # Quick standalone test
    print("Run via main.py for full comparison.")
    print("This module requires results from tfidf_clustering.py and embedding_clustering.py.")
