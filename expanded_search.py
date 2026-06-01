from query_expansion import expand_query
from search import search


def expanded_search(query, top_k=10):
    expanded_query = expand_query(query)
    return search(expanded_query, top_k=top_k)


if __name__ == "__main__":
    query = input("Enter query: ")
    results = expanded_search(query)

    for i, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"{i}. {result['title']}")
        print(f"Score: {result['score']:.4f}")
        print(f"PMID: {result['pmid']}")
        print(result["url"])