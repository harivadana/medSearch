# src/download_pubmed.py
from Bio import Entrez, Medline
import json
import os

Entrez.email = "your_email@example.com"

QUERY = """
(asthma OR COPD OR pneumonia OR bronchitis OR "pulmonary fibrosis")
AND free full text[sb]
"""

def download_pubmed_articles(retmax=1000):
    handle = Entrez.esearch(db="pubmed", term=QUERY, retmax=retmax)
    search_results = Entrez.read(handle)
    pmids = search_results["IdList"]

    fetch_handle = Entrez.efetch(
        db="pubmed",
        id=pmids,
        rettype="medline",
        retmode="text"
    )

    records = Medline.parse(fetch_handle)

    articles = []
    for record in records:
        articles.append({
            "pmid": record.get("PMID", ""),
            "title": record.get("TI", ""),
            "abstract": record.get("AB", ""),
            "journal": record.get("JT", ""),
            "year": record.get("DP", "")
        })

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/respiratory_corpus.json", "w") as f:
        json.dump(articles, f, indent=2)

    print(f"Saved {len(articles)} articles.")

if __name__ == "__main__":
    download_pubmed_articles()