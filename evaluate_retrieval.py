import csv

from search import search
from bm25_search import bm25_search
from expanded_search import expanded_search

TEST_QUERIES = [
    "shortness of breath chest tightness",
    "persistent cough wheezing asthma",
    "fever cough pneumonia",
    "pulmonary fibrosis breathing difficulty",
    "COPD chronic cough",
    "bronchitis mucus cough",
    "lung infection fever",
    "asthma wheezing children",
    "respiratory failure oxygen",
    "chest pain difficulty breathing"
]

OUTPUT_FILE = "retrieval_results_for_judging.csv"


def get_results(query, method):
    if method == "tfidf":
        return search(query, top_k=10)

    if method == "bm25":
        return bm25_search(query, top_k=10)

    if method == "expanded":
        return expanded_search(query, top_k=10)

    raise ValueError("Unknown retrieval method")


def main():
    rows = []

    methods = ["tfidf", "bm25", "expanded"]

    for method in methods:
        for query_id, query in enumerate(TEST_QUERIES, start=1):
            results = get_results(query, method)

            for rank, result in enumerate(results, start=1):
                rows.append({
                    "method": method,
                    "query_id": query_id,
                    "query": query,
                    "rank": rank,
                    "pmid": result["pmid"],
                    "title": result["title"],
                    "score": result["score"],
                    "url": result["url"],
                    "relevance": ""
                })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "method",
                "query_id",
                "query",
                "rank",
                "pmid",
                "title",
                "score",
                "url",
                "relevance"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved results to {OUTPUT_FILE}")
    print("Fill relevance manually:")
    print("0 = not relevant")
    print("1 = somewhat relevant")
    print("2 = highly relevant")


if __name__ == "__main__":
    main()