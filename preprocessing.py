import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


STOP_WORDS = set(stopwords.words("english"))

CUSTOM_STOP_WORDS = {
    "et",
    "al",
    "study",
    "studies",
    "patient",
    "patients",
    "background",
    "method",
    "methods",
    "results",
    "conclusion"
}

STOP_WORDS.update(CUSTOM_STOP_WORDS)


def preprocess_text(text):
    if not text:
        return []

    text = text.lower()

    text = re.sub(r"[^a-z\s]", " ", text)

    tokens = word_tokenize(text)

    clean_tokens = [
        token
        for token in tokens
        if token not in STOP_WORDS and len(token) > 2
    ]

    return clean_tokens