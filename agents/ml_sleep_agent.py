# agents/ml_sleep_agent.py
# ML-based Sleep Stage Predictor (HRV + Stress + HR)

import numpy as np
import joblib
import os

class MLSleepAgent:
    def __init__(self):
        model_path = os.path.join("models", "hrv_sleep_model.pkl")
        self.model = joblib.load(model_path)

    # Compute RMSSD
    def compute_rmssd(self, hr_series):
        diffs = np.diff(hr_series)
        squared = diffs ** 2
        return np.sqrt(np.mean(squared))

    # Compute SDNN
    def compute_sdnn(self, hr_series):
        return np.std(hr_series)

    def predict_stages(self, hr_series, stress_level):
        """
        hr_series: list of heart rate values for each epoch
        stress_level: 1-10
        returns: list of stages (0-4)
        """
        epochs = len(hr_series)
        features = []

        for i in range(epochs):
            # Local epoch window for HRV (3 epoch smoothing)
            window = hr_series[max(0, i-2):i+1]
            if len(window) < 2:
                window = hr_series[0:3]

            rmssd = self.compute_rmssd(window)
            sdnn = self.compute_sdnn(window)
            hr = hr_series[i]
            epoch_pos = i / epochs

            features.append([rmssd, sdnn, hr, stress_level, epoch_pos])

        X = np.array(features)
        preds = self.model.predict(X)
        return preds.tolist()
