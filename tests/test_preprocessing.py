import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from preprocessing import preprocess_text

with open(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "respiratory_corpus.json"), "r") as f:

    corpus = json.load(f)

article = corpus[0]

text = article["title"] + " " + article["abstract"]

tokens = preprocess_text(text)

print("Original Text:\n")

print(text)

print("\nTokens:\n")

print(tokens[:50])