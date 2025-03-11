"""
config.py

Project-wide configuration settings and constants.
"""

# File paths
RAW_DATA_PATH = "data/raw/input.json"
CLEANED_DATA_PATH = "data/processed/cleaned_data.csv"

EMOJI_REPLACEMENTS = {
    ':red_heart:': '[EMOJI_affection]',
    ':fire:': '[EMOJI_intensity]',
    ':smile:': '[EMOJI_happiness]',
    ':grinning:': '[EMOJI_joy]',
    ':thumbs_up:': '[EMOJI_approval]',
    ':clap:': '[EMOJI_acknowledgment]',
    ':sunglasses:': '[EMOJI_cool]',
    ':sob:': '[EMOJI_sadness]',
    ':cry:': '[EMOJI_tear]',
    ':muscle:': '[EMOJI_strength]',
    ':100:': '[EMOJI_perfection]',
    ':sparkles:': '[EMOJI_excitement]',
    ':broken_heart:': '[EMOJI_heartbreak]',
    ':star_struck:': '[EMOJI_adoration]',
    ':eyes:': '[EMOJI_attention]',
    ':winking_face:': '[EMOJI_flirtation]',
    ':blush:': '[EMOJI_embarrassment]',
    ':v:': '[EMOJI_peace]',
    ':alien:': '[EMOJI_weirdness]',
    ':sunny:': '[EMOJI_positivity]',
    ':earth_africa:': '[EMOJI_global]',
    ':trophy:': '[EMOJI_achievement]',
    ':ghost:': '[EMOJI_spooky]',
    ':robot:': '[EMOJI_technology]',
    ':rainbow:': '[EMOJI_diversity]',
    ':love_you_gesture:': '[EMOJI_affection]'
}

# Dictionary for social media shorthand expansions
SOCIAL_MEDIA_DICT = {
    "u": "you",
    "gr8": "great",
    "np": "no problem",
    "idk": "i do not know",
    "imo": "in my opinion"
}

# Additional fuzzy matching / style preserving threshold
FUZZY_MATCH_THRESHOLD = 85
