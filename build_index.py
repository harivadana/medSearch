import json
import math
import os
from collections import Counter, defaultdict

from preprocessing import preprocess_for_indexing


USE_BIOMEDICAL_ENTITIES = True


def build_index():
    with open("data/raw/respiratory_corpus.json", "r") as f:
        articles = json.load(f)

    inverted_index = defaultdict(dict)
    doc_lengths = {}
    doc_metadata = {}

    for article in articles:
        pmid = article["pmid"]
        text = f"{article['title']} {article['abstract']}"

        tokens = preprocess_for_indexing(
            text,
            use_biomedical_entities=USE_BIOMEDICAL_ENTITIES
        )

        counts = Counter(tokens)

        doc_lengths[pmid] = len(tokens)
        doc_metadata[pmid] = article

        for term, freq in counts.items():
            inverted_index[term][pmid] = freq

    num_docs = len(articles)

    idf = {
        term: math.log(num_docs / len(postings))
        for term, postings in inverted_index.items()
    }

    os.makedirs("data/processed", exist_ok=True)

    with open("data/processed/inverted_index.json", "w") as f:
        json.dump(inverted_index, f)

    with open("data/processed/idf.json", "w") as f:
        json.dump(idf, f)

    with open("data/processed/doc_metadata.json", "w") as f:
        json.dump(doc_metadata, f)

    with open("data/processed/doc_lengths.json", "w") as f:
        json.dump(doc_lengths, f)

    print(
        f"Index built. "
        f"Biomedical entities enabled: {USE_BIOMEDICAL_ENTITIES}"
    )


if __name__ == "__main__":
    build_index()