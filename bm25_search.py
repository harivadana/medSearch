import json
import math
from collections import Counter, defaultdict

from preprocessing import preprocess_for_indexing

USE_BIOMEDICAL_ENTITIES = True

INDEX_PATH = "data/processed/inverted_index.json"
METADATA_PATH = "data/processed/doc_metadata.json"
DOC_LENGTHS_PATH = "data/processed/doc_lengths.json"

K1 = 1.5
B = 0.75


def load_resources():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        inverted_index = json.load(f)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        doc_metadata = json.load(f)

    with open(DOC_LENGTHS_PATH, "r", encoding="utf-8") as f:
        doc_lengths = json.load(f)

    return inverted_index, doc_metadata, doc_lengths


def bm25_search(query, top_k=10):
    inverted_index, doc_metadata, doc_lengths = load_resources()

    query_tokens = preprocess_for_indexing(
        query,
        use_biomedical_entities=USE_BIOMEDICAL_ENTITIES
    )

    query_terms = Counter(query_tokens)

    num_docs = len(doc_metadata)
    avg_doc_length = sum(doc_lengths.values()) / num_docs

    scores = defaultdict(float)

    for term in query_terms:
        postings = inverted_index.get(term, {})

        if not postings:
            continue

        df = len(postings)
        idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1)

        for doc_id, tf in postings.items():
            doc_length = doc_lengths[doc_id]

            numerator = tf * (K1 + 1)
            denominator = tf + K1 * (
                1 - B + B * (doc_length / avg_doc_length)
            )

            scores[doc_id] += idf * (numerator / denominator)

    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    results = []

    for doc_id, score in ranked_results[:top_k]:
        article = doc_metadata[doc_id]

        results.append({
            "pmid": doc_id,
            "score": score,
            "title": article.get("title", ""),
            "abstract": article.get("abstract", ""),
            "journal": article.get("journal", ""),
            "year": article.get("year", ""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{doc_id}/"
        })

    return results