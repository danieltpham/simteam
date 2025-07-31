from pathlib import Path
import pandas as pd
from config import target_cols

def load_simteam_data(path=None):
    # Resolve default path relative to this file
    if path is None:
        path = Path(__file__).resolve().parent / "training_data" / "sim_training_data.csv"
    df = pd.read_csv(path)
    X = df.drop(columns=target_cols)
    y = df[target_cols]
    return X, y