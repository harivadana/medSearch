import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
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

    # Lowercase
    text = text.lower()

    # Remove punctuation/numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stop words + short words
    clean_tokens = [
        token
        for token in tokens
        if token not in STOP_WORDS and len(token) > 2
    ]

    return clean_tokens

_scispacy_nlp = None


def get_scispacy_pipeline():

    global _scispacy_nlp

    if _scispacy_nlp is not None:
        return _scispacy_nlp

    try:
        import spacy

        _scispacy_nlp = spacy.load("en_core_sci_sm")

    except OSError as exc:
        raise RuntimeError(
        ) from exc

    return _scispacy_nlp


def extract_biomedical_entities(text):
    """
    Extract biomedical entity phrases from text.

    Example:
    'shortness of breath'
        ->
    'ENTITY_shortness_breath'
    """

    if not text:
        return []

    nlp = get_scispacy_pipeline()

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        normalized = ent.text.lower()

        normalized = re.sub(r"[^a-z\s]", " ", normalized)

        normalized = "_".join(
            token
            for token in normalized.split()
            if token not in STOP_WORDS and len(token) > 2
        )

        if normalized:
            entities.append(f"ENTITY_{normalized}")

    return entities


def preprocess_for_indexing(
    text,
    use_biomedical_entities=False
):

    word_tokens = preprocess_text(text)

    if not use_biomedical_entities:
        return word_tokens

    entity_tokens = extract_biomedical_entities(text)

    return word_tokens + entity_tokens