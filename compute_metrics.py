import math
import pandas as pd
from collections import defaultdict

INPUT_FILE = "retrieval_results_for_judging.csv"


def precision_at_k(relevances, k=10):
    top_k = relevances[:k]
    binary_relevance = [1 if rel > 0 else 0 for rel in top_k]
    return sum(binary_relevance) / k


def average_precision(relevances):
    num_relevant = 0
    precision_sum = 0

    for i, rel in enumerate(relevances, start=1):
        if rel > 0:
            num_relevant += 1
            precision_sum += num_relevant / i

    if num_relevant == 0:
        return 0

    return precision_sum / num_relevant


def dcg_at_k(relevances, k=10):
    score = 0

    for i, rel in enumerate(relevances[:k], start=1):
        score += (2 ** rel - 1) / math.log2(i + 1)

    return score


def ndcg_at_k(relevances, k=10):
    actual_dcg = dcg_at_k(relevances, k)
    ideal_relevances = sorted(relevances, reverse=True)
    ideal_dcg = dcg_at_k(ideal_relevances, k)

    if ideal_dcg == 0:
        return 0

    return actual_dcg / ideal_dcg


def main():
    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded {len(df)} rows")

    df = df[df["relevance"].notna()]

    if len(df) == 0:
        print("No relevance judgments found.")
        print("Fill the relevance column with 0, 1, or 2 first.")
        return

    grouped = defaultdict(list)

    for _, row in df.iterrows():
        key = (row["method"], row["query_id"])
        grouped[key].append(int(row["relevance"]))

    method_scores = defaultdict(lambda: {
        "p10": [],
        "ap": [],
        "ndcg10": []
    })

    for (method, query_id), relevances in grouped.items():
        p10 = precision_at_k(relevances, k=10)
        ap = average_precision(relevances)
        ndcg10 = ndcg_at_k(relevances, k=10)

        method_scores[method]["p10"].append(p10)
        method_scores[method]["ap"].append(ap)
        method_scores[method]["ndcg10"].append(ndcg10)

        print(f"\nMethod: {method}")
        print(f"Query ID: {query_id}")
        print(f"Precision@10: {p10:.4f}")
        print(f"AP: {ap:.4f}")
        print(f"NDCG@10: {ndcg10:.4f}")

    print("\nOverall Results by Method")
    print("=" * 50)

    for method, scores in method_scores.items():
        mean_p10 = sum(scores["p10"]) / len(scores["p10"])
        map_score = sum(scores["ap"]) / len(scores["ap"])
        mean_ndcg = sum(scores["ndcg10"]) / len(scores["ndcg10"])

        print(f"\nMethod: {method}")
        print(f"Mean Precision@10: {mean_p10:.4f}")
        print(f"MAP: {map_score:.4f}")
        print(f"Mean NDCG@10: {mean_ndcg:.4f}")


if __name__ == "__main__":
    main()