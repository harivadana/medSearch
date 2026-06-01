import pandas as pd
import torch

from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

INPUT_FILE = "retrieval_results_for_judging.csv"
OUTPUT_FILE = "llm_assisted_evaluation_results.csv"

MODEL_NAME = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)

    model.eval()

    return tokenizer, model


def get_embedding(text, tokenizer, model):
    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Use CLS token embedding
    embedding = outputs.last_hidden_state[:, 0, :]

    return embedding.numpy()


def similarity_to_relevance(score):
    if score >= 0.85:
        return 2

    if score >= 0.70:
        return 1

    return 0


def main():
    df = pd.read_csv(INPUT_FILE)

    tokenizer, model = load_model()

    llm_scores = []
    llm_relevance = []

    for i, row in df.iterrows():
        query = row["query"]
        title = row["title"]

        query_embedding = get_embedding(query, tokenizer, model)
        title_embedding = get_embedding(title, tokenizer, model)

        similarity = cosine_similarity(
            query_embedding,
            title_embedding
        )[0][0]

        relevance = similarity_to_relevance(similarity)

        llm_scores.append(similarity)
        llm_relevance.append(relevance)

        print(
            f"{i + 1}/{len(df)} | "
            f"Similarity: {similarity:.4f} | "
            f"Relevance: {relevance} | "
            f"Title: {title[:70]}"
        )

    df["pubmedbert_similarity"] = llm_scores
    df["llm_assisted_relevance"] = llm_relevance

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nSaved PubMedBERT-assisted evaluation to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()