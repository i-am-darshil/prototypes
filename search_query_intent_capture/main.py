"""
Main orchestrator for the voice search query intent clustering pipeline.

Runs the full pipeline:
  1. TF-IDF clustering (monolingual baseline)
  2. Multilingual embedding clustering (cross-lingual)
  3. Evaluation and comparison
  4. Query suggestion demonstration

Usage:
    python3 main.py              # Run full pipeline
    python3 main.py --tfidf      # TF-IDF only
    python3 main.py --embedding  # Embedding only
    python3 main.py --evaluate   # Evaluate (requires both pipelines)
    python3 main.py --suggest    # Query suggestions (requires embedding pipeline)
"""

import argparse
import time

from tfidf_clustering import run_tfidf_pipeline
from embedding_clustering import run_embedding_pipeline
from evaluation import compare_approaches, generate_all_plots
from query_suggestions import run_suggestion_pipeline


def main():
    parser = argparse.ArgumentParser(description="Voice Search Query Intent Clustering")
    parser.add_argument("--tfidf", action="store_true", help="Run TF-IDF pipeline only")
    parser.add_argument("--embedding", action="store_true", help="Run embedding pipeline only")
    parser.add_argument("--evaluate", action="store_true", help="Run evaluation only (needs both pipelines)")
    parser.add_argument("--suggest", action="store_true", help="Run query suggestion demo (needs embedding pipeline)")
    args = parser.parse_args()

    run_all = not any([args.tfidf, args.embedding, args.evaluate, args.suggest])

    tfidf_results = None
    emb_results = None

    # ── Step 1: TF-IDF clustering ───────────────────────────────────────
    if run_all or args.tfidf or args.evaluate:
        t0 = time.time()
        tfidf_results = run_tfidf_pipeline()
        print(f"\n  TF-IDF pipeline completed in {time.time() - t0:.1f}s")

    # ── Step 2: Embedding clustering ────────────────────────────────────
    if run_all or args.embedding or args.evaluate or args.suggest:
        t0 = time.time()
        emb_results = run_embedding_pipeline()
        print(f"\n  Embedding pipeline completed in {time.time() - t0:.1f}s")

    # ── Step 3: Evaluation and comparison ───────────────────────────────
    if (run_all or args.evaluate) and tfidf_results and emb_results:
        print("\n")
        compare_approaches(tfidf_results, emb_results)
        generate_all_plots(tfidf_results, emb_results)

    # ── Step 4: Query suggestion demo ───────────────────────────────────
    if (run_all or args.suggest) and emb_results:
        best_k = emb_results["best_k"]
        labels = emb_results["kmeans_results"][best_k]["labels"]
        print("\n")
        run_suggestion_pipeline(
            emb_results["X"],
            emb_results["queries"],
            labels,
            emb_results["intents"],
        )

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
