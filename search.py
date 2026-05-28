# search.py

import json
import math

from collections import Counter, defaultdict

from preprocessing import preprocess_for_indexing


USE_BIOMEDICAL_ENTITIES = True

INDEX_PATH = "data/processed/inverted_index.json"
IDF_PATH = "data/processed/idf.json"
METADATA_PATH = "data/processed/doc_metadata.json"


def load_resources():

    with open(INDEX_PATH, "r") as f:
        inverted_index = json.load(f)

    with open(IDF_PATH, "r") as f:
        idf = json.load(f)

    with open(METADATA_PATH, "r") as f:
        doc_metadata = json.load(f)

    return inverted_index, idf, doc_metadata


def build_query_vector(query, idf):

    tokens = preprocess_for_indexing(
        query,
        use_biomedical_entities=USE_BIOMEDICAL_ENTITIES
    )

    counts = Counter(tokens)

    query_vector = {}

    for term, freq in counts.items():

        if term not in idf:
            continue

        tf = 1 + math.log(freq)

        query_vector[term] = tf * idf[term]

    # Normalize vector
    norm = math.sqrt(
        sum(weight ** 2 for weight in query_vector.values())
    )

    if norm == 0:
        return {}

    return {
        term: weight / norm
        for term, weight in query_vector.items()
    }


def search(query, top_k=10):

    inverted_index, idf, doc_metadata = load_resources()

    query_vector = build_query_vector(query, idf)

    if not query_vector:
        return []

    scores = defaultdict(float)

    # Compute cosine similarity
    for term, query_weight in query_vector.items():

        postings = inverted_index.get(term, {})

        for doc_id, term_freq in postings.items():

            tf = 1 + math.log(term_freq)

            doc_weight = tf * idf[term]

            scores[doc_id] += query_weight * doc_weight

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


def display_results(results):

    if not results:
        print("\nNo results found.")
        return

    for i, result in enumerate(results, start=1):

        print("\n" + "=" * 80)

        print(f"{i}. {result['title']}")

        print(f"\nScore: {result['score']:.4f}")

        print(f"Journal: {result['journal']}")

        print(f"Year: {result['year']}")

        print(f"PMID: {result['pmid']}")

        print(f"URL: {result['url']}")

        abstract_preview = result["abstract"][:500]

        print(f"\nAbstract Preview:\n{abstract_preview}...")

        print("\n" + "=" * 80)


if __name__ == "__main__":

    print("\nMedical Information Retrieval System")

    print("-----------------------------------")

    print(
        f"Biomedical entity extraction enabled: "
        f"{USE_BIOMEDICAL_ENTITIES}"
    )

    while True:

        query = input("\nEnter symptom query (or 'quit'): ")

        if query.lower() == "quit":
            break

        results = search(query)

        display_results(results)