"""
utils.py

Holds utility functions for file reading/writing and other general helpers.
"""

import pandas as pd
import json

def read_json_to_df(file_path: str) -> pd.DataFrame:
    """
    Reads a JSON file that contains a list of dict-like records and converts it into a DataFrame.
    Assumes each record has at least the fields: 'index', 'type', and 'posts'.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def write_df_to_csv(df: pd.DataFrame, file_path: str):
    """
    Writes a DataFrame to a CSV file at the specified path.
    """
    df.to_csv(file_path, index=False)
