import joblib
import json
import pandas as pd
import numpy as np
from pathlib import Path


# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"


# ─── Load Spoilage Risk (Classification) Model ────────────────────────────────

def _load_spoilage_model():
    """Load spoilage risk classification pipeline."""
    # Priority: spoilage_risk_pipeline.pkl → best_model.pkl
    for name in ["spoilage_risk_pipeline.pkl", "best_model.pkl"]:
        path = MODEL_DIR / name
        if path.exists():
            return joblib.load(path), path
    raise FileNotFoundError(
        "No spoilage risk model found in models/ folder. "
        "Please run the Jupyter notebook (post_harvest_ml_pipeline.ipynb) "
        "to train and save the model."
    )

model, _model_path = _load_spoilage_model()


# ─── Load Shelf Life (Regression) Model ───────────────────────────────────────

def _load_shelf_life_model():
    """Load shelf life regression pipeline (optional)."""
    path = MODEL_DIR / "shelf_life_pipeline.pkl"
    if path.exists():
        return joblib.load(path)
    return None

shelf_life_model = _load_shelf_life_model()


# ─── Feature Columns ──────────────────────────────────────────────────────────

# Extract expected feature column names directly from the Pipeline model
if hasattr(model, "feature_names_in_"):
    feature_columns = list(model.feature_names_in_)
else:
    feature_columns = [
        "Category", "Produce_Name", "Variety", "Produce_Grade", "Quality_Score",
        "Health_Score", "Market_Price", "Transport_Mode", "Distance_to_Market",
        "Cold_Chain_Available", "Sensor_Battery_Level", "GPS_Latitude", "GPS_Longitude",
        "Market_Demand", "Storage_Cost", "State", "District", "Storage_Type",
        "Package_Type", "Storage_Duration", "Temperature", "Humidity", "Light_Intensity",
        "CO2_Level", "Ethylene_Level", "Moisture_Content", "Weight", "Weather",
        "Season", "Disease_Detected", "Sensor_Status"
    ]


# ─── Load Model Info ──────────────────────────────────────────────────────────

def get_model_info():
    """
    Return model metadata from active_model.json and training_report.json.
    Safe to call even if files are missing.
    """
    info = {
        "model_name": "Random Forest Pipeline",
        "model_file": str(_model_path.name),
        "accuracy": None,
        "trained_at": None,
        "source": "post_harvest_ml_pipeline.ipynb",
        "shelf_life_model_available": shelf_life_model is not None,
    }

    # Try active_model.json
    active_path = MODEL_DIR / "active_model.json"
    if active_path.exists():
        try:
            with open(active_path, "r") as f:
                data = json.load(f)
            info.update({
                "model_name": data.get("best_model", info["model_name"]),
                "accuracy": data.get("accuracy"),
                "trained_at": data.get("trained_at"),
                "source": data.get("pipeline_source", info["source"]),
            })
        except Exception:
            pass

    # Try training_report.json for extra metrics
    report_path = MODEL_DIR / "training_report.json"
    if report_path.exists():
        try:
            with open(report_path, "r") as f:
                report = json.load(f)
            info.update({
                "precision": report.get("precision"),
                "recall": report.get("recall"),
                "f1_score": report.get("f1_score"),
                "dataset_rows": report.get("dataset_rows"),
                "features_used": report.get("features_used"),
                "shelf_life_r2": report.get("shelf_life_metrics", {}).get("r2_score"),
                "shelf_life_mae": report.get("shelf_life_metrics", {}).get("mae_days"),
            })
        except Exception:
            pass

    return info


# ─── Helper: Prepare DataFrame for Pipeline ───────────────────────────────────

def _prepare_dataframe(df):
    """
    Ensures input dataframe contains all required features aligned to the
    Pipeline model. Handles column name normalization and missing feature
    backfilling.
    """
    df = df.copy()

    # Column header normalization & mapping
    normalized_existing = {
        str(col).strip().lower().replace(" ", "_").replace("-", "_"): col
        for col in df.columns
    }

    rename_map = {}
    for feature in feature_columns:
        norm_feat = feature.lower().replace(" ", "_").replace("-", "_")
        if feature not in df.columns and norm_feat in normalized_existing:
            rename_map[normalized_existing[norm_feat]] = feature

    if rename_map:
        df = df.rename(columns=rename_map)

    # Ensure all required feature columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    return df[feature_columns]


# ─── Helper: Risk Level Mapping ───────────────────────────────────────────────

def _get_risk_level(prediction_text, confidence=None):
    """Maps model output class to risk level string."""
    label = str(prediction_text).strip()
    label_lower = label.lower()

    if label_lower in ["high", "medium", "low"]:
        return label.capitalize()
    elif "spoil" in label_lower or "bad" in label_lower or "critical" in label_lower:
        return "High"
    elif "fresh" in label_lower or "good" in label_lower or "normal" in label_lower:
        return "Low"
    elif "warning" in label_lower or "moderate" in label_lower:
        return "Medium"

    return label


# ─── Single Prediction ────────────────────────────────────────────────────────

def predict(input_data):
    """
    Generates spoilage risk prediction for a single record dict using the
    Scikit-Learn Pipeline trained in post_harvest_ml_pipeline.ipynb.

    Returns:
        (prediction_text, confidence, risk_level)
    """
    input_df = pd.DataFrame([input_data])
    prepared_df = _prepare_dataframe(input_df)

    prediction = model.predict(prepared_df)[0]

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(prepared_df)[0]
        confidence = float(np.max(probabilities) * 100)
    else:
        confidence = 100.0

    prediction_text = str(prediction)
    risk_level = _get_risk_level(prediction_text, confidence)

    return (prediction_text, confidence, risk_level)


# ─── Shelf Life Prediction ────────────────────────────────────────────────────

def predict_shelf_life(input_data):
    """
    Predicts shelf life (in days) for a single record dict using the
    regression pipeline trained in post_harvest_ml_pipeline.ipynb.

    Returns:
        float (predicted days) or None if model unavailable
    """
    if shelf_life_model is None:
        return None

    input_df = pd.DataFrame([input_data])
    prepared_df = _prepare_dataframe(input_df)

    try:
        days = float(shelf_life_model.predict(prepared_df)[0])
        return round(days, 1)
    except Exception:
        return None


# ─── Bulk Prediction ──────────────────────────────────────────────────────────

def predict_bulk(input_df):
    """
    Generates batch predictions for a DataFrame using the Scikit-Learn Pipeline
    trained in post_harvest_ml_pipeline.ipynb.

    Returns:
        result_df with columns: Prediction, Confidence, Risk Level,
        and optionally Predicted_Shelf_Life_Days
    """
    if input_df is None or input_df.empty:
        raise ValueError("Input dataframe is empty.")

    original_df = input_df.copy()
    prepared_df = _prepare_dataframe(original_df)

    predictions = model.predict(prepared_df)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(prepared_df)
        confidence_values = np.max(probabilities, axis=1) * 100
    else:
        confidence_values = np.full(len(predictions), 100.0)

    prediction_labels = [str(val) for val in predictions]
    risk_levels = [
        _get_risk_level(pred, conf)
        for pred, conf in zip(prediction_labels, confidence_values)
    ]

    result_df = original_df.copy()
    result_df["Prediction"] = prediction_labels
    result_df["Confidence"] = np.round(confidence_values, 2)
    result_df["Risk Level"] = risk_levels

    # Add shelf life predictions if model available
    if shelf_life_model is not None:
        try:
            shelf_days = shelf_life_model.predict(prepared_df)
            result_df["Predicted_Shelf_Life_Days"] = np.round(shelf_days, 1)
        except Exception:
            pass

    return result_df
