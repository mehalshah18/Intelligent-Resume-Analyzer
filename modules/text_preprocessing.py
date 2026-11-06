
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


# Download stopwords if they are not available
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))


# Tokenizer that preserves technical terms such as C++, C#, etc.
tokenizer = RegexpTokenizer(
    r"[a-z0-9]+(?:[+#.][a-z0-9+#.]*)*"
)


def clean_text(text):
    """
    Clean unnecessary content from resume text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

    # Remove extra spaces and line breaks
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def tokenize_text(text):
    """
    Divide text into individual tokens.
    """

    tokens = tokenizer.tokenize(text)

    return tokens


def remove_stopwords(tokens):
    """
    Remove common English words.
    """

    filtered_tokens = [
        word for word in tokens
        if word not in STOP_WORDS
    ]

    return filtered_tokens


def preprocess_text(text):
    """
    Complete NLP preprocessing pipeline.
    """

    cleaned_text = clean_text(text)

    tokens = tokenize_text(cleaned_text)

    filtered_tokens = remove_stopwords(tokens)

    processed_text = " ".join(filtered_tokens)

    return {
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "processed_text": processed_text
    }
