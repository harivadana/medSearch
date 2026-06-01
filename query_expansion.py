MEDICAL_SYNONYMS = {
    "cough": ["coughing"],
    "cold": ["upper respiratory infection", "common cold"],
    "fever": ["pyrexia", "high temperature"],
    "wheezing": ["wheeze", "bronchospasm"],
    "asthma": ["bronchial asthma"],
    "copd": ["chronic obstructive pulmonary disease"],
    "pneumonia": ["lung infection"],
    "bronchitis": ["airway inflammation"],
    "shortness": ["dyspnea"],
    "breath": ["breathing"],
    "chest": ["thoracic"],
    "tightness": ["pressure"],
    "pulmonary": ["lung"],
    "fibrosis": ["scarring"],
    "respiratory": ["breathing", "pulmonary"]
}


def expand_query(query):
    tokens = query.lower().split()

    expanded_terms = list(tokens)

    for token in tokens:
        if token in MEDICAL_SYNONYMS:
            expanded_terms.extend(MEDICAL_SYNONYMS[token])

    return " ".join(expanded_terms)


if __name__ == "__main__":
    query = "shortness of breath cough"
    print("Original:", query)
    print("Expanded:", expand_query(query))