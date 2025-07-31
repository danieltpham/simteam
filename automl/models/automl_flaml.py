from flaml.automl import AutoML
from sklearn.base import BaseEstimator, RegressorMixin
import numpy as np
import joblib
import os

class MultiOutputFLAML(BaseEstimator, RegressorMixin):
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.models = []

    def fit(self, X, Y):
        self.models = []
        for col in Y.columns:
            model = AutoML()
            model.fit(X, Y[col], **self.settings)
            self.models.append(model)
        return self

    def predict(self, X):
        return np.stack([m.predict(X) for m in self.models], axis=1)

    def save(self, path: str):
        """
        Save the model list and settings to the given path.
        This creates a directory with separate files per target model.
        """
        os.makedirs(path, exist_ok=True)
        for i, model in enumerate(self.models):
            joblib.dump(model, os.path.join(path, f"model_{i}.joblib"))
        joblib.dump(self.settings, os.path.join(path, "settings.joblib"))

    @classmethod
    def load(cls, path: str):
        """
        Load a MultiOutputFLAML model from a saved directory.
        """
        settings = joblib.load(os.path.join(path, "settings.joblib"))
        model = cls(settings=settings)

        i = 0
        loaded_models = []
        while True:
            model_path = os.path.join(path, f"model_{i}.joblib")
            if not os.path.exists(model_path):
                break
            loaded_models.append(joblib.load(model_path))
            i += 1

        model.models = loaded_models
        return model
