"""
Shared data loading utility.
Loads the multilingual voice search CSV and extracts query texts + metadata.
"""

import pandas as pd

DATA_PATH = "voice_search_query_captures_multilingual.csv"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load the full dataset."""
    df = pd.read_csv(path)
    return df


def get_queries_and_labels(path: str = DATA_PATH) -> tuple[pd.DataFrame, list[str], list[str]]:
    """
    Load data and return (dataframe, query_texts, true_intents).
    true_intents can be used for external validation of clusters.
    """
    df = load_data(path)
    queries = df["query_text"].astype(str).tolist()
    intents = df["intent"].astype(str).tolist()
    return df, queries, intents


if __name__ == "__main__":
    df, queries, intents = get_queries_and_labels()
    print(f"Loaded {len(queries)} queries ({df['query_text'].nunique()} unique)")
    print(f"Intents: {pd.Series(intents).value_counts().to_dict()}")
    print(f"Languages: {df['language'].value_counts().to_dict()}")
    print(f"\nSample queries:")
    for q in queries[:5]:
        print(f"  {q}")
