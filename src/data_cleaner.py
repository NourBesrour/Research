"""
data_cleaner.py

Implements a class-based data cleaning pipeline tailored for MBTI classification
with BERT. It handles:
- HTML tag removal
- Hashtag normalization
- Mention tokenization
- Emoji translation
- Social media abbreviation handling  
- Minimal spelling correction
- Punctuation, mention, and hashtag feature preservation
- URL tokenization (domain-centric approach)

We avoid overly-aggressive text normalization to preserve psycho-linguistic signals.
"""

import re
import html
import emoji
from urllib.parse import urlparse
from typing import List
from fuzzywuzzy import fuzz
from symspellpy import SymSpell, Verbosity

from .config import EMOJI_REPLACEMENTS, SOCIAL_MEDIA_DICT, FUZZY_MATCH_THRESHOLD
from .config import RAW_DATA_PATH, CLEANED_DATA_PATH
from .utils import read_json_to_df, write_df_to_csv


class MBTICleaner:
    """
    MBTICleaner is a data cleaning pipeline that preserves psycho-linguistic
    signals in social media text for MBTI classification using BERT.
    """

    def __init__(self):
        """
        Initialize any resource-intensive components like spelling checkers,
        frequency dictionaries, etc.
        """
        # Initialize SymSpell for context-aware spelling checks
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        # For demonstration, we won't add a dictionary file here, but in practice,
        # you should load a dictionary for proper spelling corrections:
        # self.sym_spell.load_dictionary("path/to/frequency_dictionary.txt", 0, 1)

    def clean_posts(self, texts: List[str]) -> List[str]:
        """
        Applies a series of text transformations to preserve meaningful features
        while reducing noise.
        """
        cleaned_texts = []
        for text in texts:
            # 1. Unescape HTML entities (e.g., &amp; -> &)
            text = html.unescape(text)

            # 2. Remove leftover HTML tags if any
            text = re.sub(r"<[^>]+>", "", text)

            # 3. Handle Mentions (@username).
            text = re.sub(r"@\w+", "[MENTION]", text)

            # 4. Hashtag Normalization
            text = self._normalize_hashtags(text)

            # 5. Emoji Preservation via demojize
            text = emoji.demojize(text, language="en")
            for emo_key, emo_val in EMOJI_REPLACEMENTS.items():
                text = text.replace(emo_key, emo_val)

            # 6. Convert common social media abbreviations
            text = self._expand_social_media_slang(text)

            # 7. Controlled spelling correction.
            text = self._spell_check_text(text)

            # 8. Remove excessive repeated characters but keep some for stylistic nuance
            text = re.sub(r"(.)\1{3,}", r"\1\1", text)

            # 9. URL Tokenization (domain-centric)
            text = self._tokenize_urls(text)

            # 10. Optional: Lower-case standardization
            text = text.lower()

            # 11. Trim extra whitespace
            text = re.sub(r"\s+", " ", text).strip()

            cleaned_texts.append(text)

        return cleaned_texts

    def _normalize_hashtags(self, text: str) -> str:
        def split_hashtag(hashtag):
            return re.sub(r"([A-Z][a-z]+)", r" \1", hashtag).strip().replace("  ", " ")

        matches = re.findall(r"#\w+", text)
        for match in matches:
            term = match[1:]
            replacement = split_hashtag(term)
            text = text.replace(match, replacement)
        return text

    def _expand_social_media_slang(self, text: str) -> str:
        words = text.split()
        expanded_words = [SOCIAL_MEDIA_DICT.get(word, word) for word in words]
        return " ".join(expanded_words)

    def _spell_check_text(self, text: str) -> str:
        words = text.split()
        corrected_words = [w if "[MENTION]" in w or "[EMOJI" in w else w for w in words]
        return " ".join(corrected_words)

    def _tokenize_urls(self, text: str) -> str:
        matches = re.findall(r"https?://\S+", text)
        for url in matches:
            try:
                parsed = urlparse(url)
                domain_parts = parsed.hostname.split('.') if parsed.hostname else []
                path_parts = parsed.path.split('/')[1:]
                replacement = " ".join(["[URL]"] + domain_parts + ["[PATH]"] + path_parts)
                text = text.replace(url, replacement)
            except ValueError:
                print(f"Skipping malformed URL: {url}")
                text = text.replace(url, "[URL] malformed")
        return text

    def process_dataframe(self, df):
        """
        Apply the cleaning pipeline to the 'posts' column of the DataFrame.
        Returns a new DataFrame with the cleaned posts in 'cleaned_posts'.
        """
        df["cleaned_posts"] = self.clean_posts(df["body"].tolist())
        return df

    def run(self):
        """
        1) Load the raw data from JSON
        2) Clean the posts
        3) Save the cleaned data to CSV
        """
        df = read_json_to_df(RAW_DATA_PATH)
        df_cleaned = self.process_dataframe(df)
        write_df_to_csv(df_cleaned, CLEANED_DATA_PATH)
        print(f"Cleaned data saved to {CLEANED_DATA_PATH}")