import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
from pathlib import Path

from data_loader import load_simteam_data
from models.automl_flaml import MultiOutputFLAML
from config import automl_settings, target_cols


class SurrogateTrainer:
    def __init__(self, model_path="models/flaml_pipeline.joblib", settings=None):
        self.model_path = Path(model_path)
        self.settings = settings or automl_settings
        self.pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("automl", MultiOutputFLAML(settings=self.settings))
        ])

    def train_with_cv(self, n_splits=10, random_state=42):
        X, y = load_simteam_data()
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        rmse_scores = []

        for train_idx, test_idx in kf.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            self.pipeline.fit(X_train, y_train)
            preds = self.pipeline.predict(X_test)
            fold_rmse = np.sqrt(((preds - y_test.values) ** 2).mean(axis=0))
            rmse_scores.append(fold_rmse)

        return pd.DataFrame({
            "target": target_cols,
            "RMSE_CV10": np.mean(rmse_scores, axis=0)
        })

    def fit_full(self):
        X, y = load_simteam_data()
        self.pipeline.fit(X, y)

    def save(self):
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        dump(self.pipeline, self.model_path)

    def load(self):
        self.pipeline = load(self.model_path)

    def predict(self, X_new):
        return self.pipeline.predict(X_new)
