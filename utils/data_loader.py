import pandas as pd
import os

def load_hospitals(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Hospital dataset is empty")

    # Normalize city names for matching
    df["city"] = df["city"].astype(str).str.strip().str.lower()

    return df


def filter_by_city(df, city):
    city = city.strip().lower()

    # partial match (handles goa / panaji / etc.)
    filtered = df[df["city"].str.contains(city)]

    return filtered
