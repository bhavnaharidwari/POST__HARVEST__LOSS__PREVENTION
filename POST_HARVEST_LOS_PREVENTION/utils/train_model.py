import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# Train Uploaded Dataset using Pipeline


def train_uploaded_dataset(dataset_path, target_column=None):
    # Load Dataset
    df = pd.read_csv(dataset_path)
    df = df.drop_duplicates()
    df = df.ffill().bfill()

    target_candidates = [
        "Spoilage_Status", "Spoilage", "Status", "Target",
        "Prediction", "Freshness", "Risk", "Label", "Class", "Spoilage_Risk"
    ]

    if target_column is not None:
        actual_target = None
        for col in df.columns:
            if col.strip().lower() == target_column.strip().lower():
                actual_target = col
                break
        if actual_target is None:
            raise Exception(f"Selected target column '{target_column}' not found.")
        target_column = actual_target
    else:
        detected = None
        for col in df.columns:
            for candidate in target_candidates:
                if col.strip().lower() == candidate.lower():
                    detected = col
                    break
            if detected is not None:
                break
        if detected is None:
            raise Exception("Target column not found.")
        target_column = detected

    X = df.drop(columns=[target_column]).copy()
    y = df[target_column].astype(str).str.strip().copy()

    # Identify numeric and categorical columns
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), cat_cols)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    classifiers = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }

    results = {}
    best_pipeline = None
    best_name = None
    best_accuracy = 0

    for model_name, clf in classifiers.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        results[model_name] = round(accuracy * 100, 2)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_pipeline = pipeline
            best_name = model_name

    BASE_DIR = Path(__file__).resolve().parent.parent
    MODEL_DIR = BASE_DIR / "models"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Save Single Pipeline PKL File
    joblib.dump(best_pipeline, MODEL_DIR / "custom_model.pkl")

    feature_columns = list(X.columns)
    dataset_name = Path(dataset_path).name
    trained_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    report = {
        "dataset_name": dataset_name,
        "dataset_rows": int(len(df)),
        "dataset_columns": int(len(df.columns)),
        "target_column": target_column,
        "best_model": best_name,
        "accuracy": round(best_accuracy * 100, 2),
        "results": results,
        "trained_at": trained_at
    }

    with open(MODEL_DIR / "training_report.json", "w") as file:
        json.dump(report, file, indent=4)

    active_model = {
        "model_type": "uploaded",
        "model_status": "active",
        "model_file": "custom_model.pkl",
        "dataset_name": dataset_name,
        "target_column": target_column,
        "best_model": best_name,
        "accuracy": round(best_accuracy * 100, 2),
        "trained_at": trained_at
    }

    with open(MODEL_DIR / "active_model.json", "w") as file:
        json.dump(active_model, file, indent=4)

    return {
        "best_model": best_name,
        "accuracy": round(best_accuracy * 100, 2),
        "results": results,
        "dataset_name": dataset_name,
        "target_column": target_column,
        "model_type": "uploaded",
        "status": "active",
        "trained_at": trained_at
    }