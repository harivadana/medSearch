import pandas as pd
import re

INPUT_FILE = "retrieval_results_for_judging.csv"
OUTPUT_FILE = "retrieval_results_for_judging.csv"

RESPIRATORY_TERMS = {
    "asthma", "cough", "coughing", "wheezing", "wheeze",
    "pneumonia", "bronchitis", "copd", "pulmonary", "lung",
    "respiratory", "breath", "breathing", "oxygen", "fibrosis",
    "infection", "sputum", "airway", "inhaled", "chest",
    "dyspnea", "rsv", "mycoplasma"
}

QUERY_SYNONYMS = {
    "copd": {"chronic", "obstructive", "pulmonary", "disease"},
    "shortness": {"breath", "breathing", "dyspnea"},
    "breath": {"breathing", "dyspnea", "respiratory"},
    "cold": {"respiratory", "infection", "virus"},
    "lung": {"pulmonary", "respiratory"},
    "pneumonia": {"mycoplasma", "infection", "pulmonary"},
}


def tokenize(text):
    text = str(text).lower()
    return set(re.findall(r"[a-z]+", text))


def expanded_query_terms(query):
    terms = tokenize(query)
    expanded = set(terms)

    for term in terms:
        if term in QUERY_SYNONYMS:
            expanded.update(QUERY_SYNONYMS[term])

    return expanded


def assign_relevance(query, title):
    query_terms = expanded_query_terms(query)
    title_terms = tokenize(title)

    overlap = query_terms.intersection(title_terms)
    respiratory_matches = title_terms.intersection(RESPIRATORY_TERMS)

    if len(overlap) >= 2:
        return 2

    if len(overlap) == 1 and len(respiratory_matches) >= 1:
        return 2

    if len(respiratory_matches) >= 2:
        return 1

    if len(respiratory_matches) == 1:
        return 1

    return 0


def main():
    df = pd.read_csv(INPUT_FILE)

    df["relevance"] = df.apply(
        lambda row: assign_relevance(row["query"], row["title"]),
        axis=1
    )

    df.to_csv(OUTPUT_FILE, index=False)

    print("Relevance labels filled automatically.")
    print(df["relevance"].value_counts().sort_index())


if __name__ == "__main__":
    main()