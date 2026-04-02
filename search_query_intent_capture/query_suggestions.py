"""
Query suggestion and retrieval grouping module.

Demonstrates how clustering improves:
  1. Query suggestions — given an input query, suggest related queries from the same cluster
  2. Retrieval grouping — group search results by discovered intent clusters
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from data_loader import get_queries_and_labels
from embedding_clustering import MODEL_NAME


# Query suggestion engine
class ClusterBasedSuggester:
    """
    Suggests related queries by:
      1. Finding which cluster the input query belongs to
      2. Returning the most similar queries within that cluster

    This is better than naive nearest-neighbour because:
      - It constrains suggestions to the same intent group
      - It works across languages (multilingual embeddings)
      - It's faster at scale (search within cluster, not entire corpus)
    """

    def __init__(self, embeddings: np.ndarray, queries: list[str], labels: np.ndarray, model_name: str = MODEL_NAME):
        self.embeddings = embeddings
        self.queries = queries
        self.labels = labels
        self.model = SentenceTransformer(model_name)

        # Pre-compute cluster membership
        self.cluster_indices = {}
        for idx, cid in enumerate(labels):
            if cid == -1:
                continue
            self.cluster_indices.setdefault(cid, []).append(idx)

    def suggest(self, query: str, top_k: int = 5, same_cluster_only: bool = True) -> list[dict]:
        """
        Given an input query, return top_k suggestions.

        Returns list of {query, similarity, cluster} dicts.
        """
        q_emb = self.model.encode([query])

        if same_cluster_only:
            # Find nearest cluster centroid
            cluster_id = self._find_cluster(q_emb)
            candidate_indices = self.cluster_indices.get(cluster_id, [])
            if not candidate_indices:
                # Fallback to all
                candidate_indices = list(range(len(self.queries)))
        else:
            candidate_indices = list(range(len(self.queries)))

        candidate_embeddings = self.embeddings[candidate_indices]
        sims = cosine_similarity(q_emb, candidate_embeddings)[0]

        # Deduplicate by query text, keeping highest similarity
        seen = {}
        for i, sim in enumerate(sims):
            q_text = self.queries[candidate_indices[i]]
            if q_text not in seen or sim > seen[q_text]["similarity"]:
                seen[q_text] = {
                    "query": q_text,
                    "similarity": float(sim),
                    "cluster": int(self.labels[candidate_indices[i]]),
                }

        ranked = sorted(seen.values(), key=lambda x: x["similarity"], reverse=True)
        return ranked[:top_k]

    def _find_cluster(self, q_emb: np.ndarray) -> int:
        """Find the cluster whose centroid is closest to the query embedding."""
        best_cluster = -1
        best_sim = -1
        for cid, indices in self.cluster_indices.items():
            centroid = self.embeddings[indices].mean(axis=0, keepdims=True)
            sim = cosine_similarity(q_emb, centroid)[0, 0]
            if sim > best_sim:
                best_sim = sim
                best_cluster = cid
        return best_cluster


# Retrieval grouping
def group_queries_by_cluster(queries: list[str], labels: np.ndarray, intents: list[str]) -> dict:
    """
    Group queries by cluster, showing how clustering organises
    diverse queries into coherent intent groups.
    """
    groups = {}
    for i, (q, cid, intent) in enumerate(zip(queries, labels, intents)):
        if cid == -1:
            continue
        cid = int(cid)
        if cid not in groups:
            groups[cid] = {"queries": [], "intents": []}
        groups[cid]["queries"].append(q)
        groups[cid]["intents"].append(intent)

    # Summarise each group
    for cid in groups:
        from collections import Counter
        intent_counts = Counter(groups[cid]["intents"])
        dominant = intent_counts.most_common(1)[0]
        unique_queries = list(set(groups[cid]["queries"]))
        groups[cid]["dominant_intent"] = dominant[0]
        groups[cid]["purity"] = dominant[1] / len(groups[cid]["intents"])
        groups[cid]["unique_queries"] = unique_queries
        groups[cid]["size"] = len(groups[cid]["queries"])

    return groups


# Demonstration
def demonstrate_suggestions(embeddings: np.ndarray, queries: list[str], labels: np.ndarray):
    """Run demonstration of cluster-based query suggestions."""
    print("=" * 60)
    print("QUERY SUGGESTION DEMONSTRATION")
    print("=" * 60)

    suggester = ClusterBasedSuggester(embeddings, queries, labels)

    # Test queries — mix of English and multilingual
    test_queries = [
        "Play some music",
        "How do I get to the mall?",
        "Order food online",
        "What's the temperature outside?",
        "Set a timer",
        "Compra algo en línea",        # Spanish: Buy something online
        "最近のニュースを教えて",         # Japanese: Tell me recent news
        "Wie wird das Wetter morgen?",  # German: How's the weather tomorrow?
    ]

    for test_q in test_queries:
        print(f"\n  Query: \"{test_q}\"")

        # Cluster-constrained suggestions
        suggestions = suggester.suggest(test_q, top_k=5, same_cluster_only=True)
        print(f"  Cluster-based suggestions:")
        for s in suggestions:
            print(f"    [{s['cluster']}] {s['query']} (sim={s['similarity']:.3f})")

        # Unconstrained (naive) suggestions for comparison
        naive = suggester.suggest(test_q, top_k=5, same_cluster_only=False)
        print(f"  Naive nearest-neighbour:")
        for s in naive:
            print(f"    [{s['cluster']}] {s['query']} (sim={s['similarity']:.3f})")


def demonstrate_retrieval_grouping(queries: list[str], labels: np.ndarray, intents: list[str]):
    """Show how clustering organises queries into retrieval groups."""
    print("\n" + "=" * 60)
    print("RETRIEVAL GROUPING DEMONSTRATION")
    print("=" * 60)

    groups = group_queries_by_cluster(queries, labels, intents)

    print(f"\n  {len(groups)} clusters discovered:\n")
    for cid in sorted(groups):
        g = groups[cid]
        print(f"  Cluster {cid} — \"{g['dominant_intent']}\" (purity={g['purity']:.1%}, size={g['size']})")
        print(f"    Sample queries:")
        for q in g["unique_queries"][:6]:
            print(f"      - {q}")
        print()

    # within-cluster query diversity
    print("  KEY INSIGHT: Clustering groups semantically similar queries across")
    print("  languages, surface forms, and phrasings into coherent intent buckets.")
    print("  This enables:")
    print("    1. Intent-aware suggestions (suggest within same intent cluster)")
    print("    2. Multilingual query expansion (find equivalent queries in other languages)")
    print("    3. Retrieval re-ranking (boost results matching the query's cluster intent)")


def run_suggestion_pipeline(embeddings: np.ndarray, queries: list[str], labels: np.ndarray, intents: list[str]):
    """Full suggestion + retrieval grouping pipeline."""
    demonstrate_suggestions(embeddings, queries, labels)
    demonstrate_retrieval_grouping(queries, labels, intents)


if __name__ == "__main__":
    print("Run via main.py for full pipeline.")
    print("This module requires embeddings and cluster labels from embedding_clustering.py.")
