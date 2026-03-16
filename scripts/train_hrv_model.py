# scripts/train_hrv_model.py
# Train a RandomForest model on synthetic HRV features and save to models/hrv_sleep_model.pkl

import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Ensure models folder exists
os.makedirs("../models", exist_ok=True)

def generate_sample(epochs=100):
    """
    Generate HRV-like features and synthetic sleep stages.
    """
    X = []
    y = []
    for i in range(epochs):
        # Features
        rmssd = np.random.normal(40, 12)
        sdnn  = np.random.normal(60, 20)
        hr    = np.random.normal(70, 8)
        stress = np.random.uniform(1, 10)
        epoch_pos = i / epochs

        # Stage probabilities based on epoch progression
        if epoch_pos < 0.1:
            probs = [0.2, 0.3, 0.35, 0.1, 0.05]
        elif epoch_pos < 0.6:
            probs = [0.05, 0.15, 0.45, 0.25, 0.10]
        else:
            probs = [0.05, 0.15, 0.35, 0.15, 0.30]

        stage = np.random.choice([0,1,2,3,4], p=probs)

        X.append([rmssd, sdnn, hr, stress, epoch_pos])
        y.append(stage)

    return np.array(X), np.array(y)

# Build dataset
X_list = []
Y_list = []

for _ in range(300):
    Xn, yn = generate_sample(100)
    X_list.append(Xn)
    Y_list.append(yn)

X = np.vstack(X_list)
y = np.hstack(Y_list)

print("Dataset shape:", X.shape, y.shape)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)

# RandomForest
model = RandomForestClassifier(
    n_estimators=250,
    max_depth=18,
    random_state=42
)
model.fit(X_train, y_train)

print("Test Accuracy:", model.score(X_test, y_test))

# Save model
joblib.dump(model, "../models/hrv_sleep_model.pkl")
print("Model saved → ../models/hrv_sleep_model.pkl")
