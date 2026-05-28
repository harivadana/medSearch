<p align="center">

  <img src="https://img.shields.io/badge/Biomedical-Information%20Retrieval-blue?style=for-the-badge" />

  <img src="https://img.shields.io/badge/Python-IR%20System-green?style=for-the-badge" />

  <img src="https://img.shields.io/badge/scispaCy-Biomedical%20NLP-orange?style=for-the-badge" />

</p>

<h1 align="center">

🩺 medSearch

</h1>

<p align="center">

Biomedical Information Retrieval System for Respiratory Disease Literature

</p>

<p align="center">

Built using TF-IDF, Inverted Indexing, Cosine Similarity, and Biomedical NLP

</p>

---
# medSearch

medSearch is a biomedical information retrieval (IR) system focused on respiratory disease literature. The project builds a searchable corpus from PubMed abstracts and supports symptom-based querying using classical information retrieval techniques such as inverted indexes, TF-IDF weighting, cosine similarity retrieval, and biomedical entity extraction using scispaCy.

---

# Features

- PubMed biomedical corpus construction
- Respiratory disease literature retrieval
- NLTK-based preprocessing and stop-word removal
- Biomedical entity extraction using scispaCy
- Inverted index generation
- TF-IDF vector weighting
- Cosine similarity ranking
- Query-based medical document retrieval
- Retrieval evaluation using Precision, MAP, and NDCG

---

# Project Structure

text medSearch/ ├── data/ │   ├── raw/ │   └── processed/ ├── tests/ ├── build_index.py ├── download_documents.py ├── preprocessing.py ├── search.py ├── evaluate_retrieval.py ├── compute_metrics.py ├── requirements.txt └── README.md 

---

# Installation

## 1. Clone Repository

bash git clone https://github.com/yassir20191/medSearch.git cd medSearch 

---

## 2. Create Virtual Environment

### Mac/Linux

bash python3 -m venv venv source venv/bin/activate 

### Windows

bash python -m venv venv venv\Scripts\activate 

---

## 3. Upgrade pip

bash python3 -m pip install --upgrade pip setuptools wheel 

---

## 4. Install Biomedical NLP Model

bash python3 -m pip install \ https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.5/en_core_sci_sm-0.5.5-py3-none-any.whl 

---

## 5. Install Dependencies

bash python3 -m pip install -r requirements.txt 

---

# Building the Biomedical Corpus

Run the PubMed downloader:

bash python3 download_documents.py 

This downloads respiratory disease abstracts and metadata into:

text data/raw/respiratory_corpus.json 

---

# Building the Inverted Index

Inside build_index.py:

python USE_BIOMEDICAL_ENTITIES = True 

Then run:

bash python3 build_index.py 

This generates:

text data/processed/ ├── inverted_index.json ├── idf.json ├── doc_metadata.json └── doc_lengths.json 

---

# Running the Search Engine

Run:

bash python3 search.py 

Example queries:

text shortness of breath 

text persistent cough wheezing 

text pulmonary fibrosis chest tightness 

---

# Biomedical Entity Extraction

The system optionally uses scispaCy biomedical entity extraction to preserve important medical phrases during indexing and querying.

Example:

text shortness of breath     -> ENTITY_shortness_breath  pulmonary fibrosis     -> ENTITY_pulmonary_fibrosis 

This improves retrieval quality for multi-word medical concepts.

---

# Retrieval Pipeline

text PubMed Documents         ↓ Preprocessing         ↓ Tokenization         ↓ Stop-word Removal         ↓ Biomedical Entity Extraction         ↓ Inverted Index Construction         ↓ TF-IDF Weighting         ↓ Cosine Similarity Retrieval 

---

# Evaluating the IR System

## Generate Evaluation Results

Create retrieval outputs for manual judging:

bash python3 evaluate_retrieval.py 

This creates:

text retrieval_results_for_judging.csv 

Manually assign relevance scores:

text 0 = not relevant 1 = somewhat relevant 2 = highly relevant 

---

## Compute Metrics

Run:

bash python3 compute_metrics.py 

Metrics include:

- Precision@10
- MAP (Mean Average Precision)
- NDCG@10

---

# Research Focus

This project explores biomedical information retrieval and symptom-oriented document search using classical IR techniques enhanced with biomedical NLP preprocessing.

The project is inspired by retrieval-based medical decision support systems such as CliniqIR and investigates how biomedical entity extraction can improve symptom-based medical literature retrieval.

---

# Future Improvements
