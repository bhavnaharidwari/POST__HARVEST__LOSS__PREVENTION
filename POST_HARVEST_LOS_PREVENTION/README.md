# 🌾 Post-Harvest Loss Prevention System

An AI-powered decision-support web app that predicts **spoilage risk** and estimates **shelf life** of fruits and vegetables from storage conditions, produce characteristics and environmental data. It helps farmers, warehouse managers and distributors act *before* produce spoils.

Built with **Python, Streamlit, scikit-learn, Plotly and SQLite**.

---

## ✨ Features

| Module | What it does |
|---|---|
| **Dashboard** | Project overview and current weather snapshot (temperature, humidity, wind, location). |
| **Dataset** | Interactive analytics on the produce dataset: KPI cards, smart filters, search, statistics, correlation, missing-value and outlier analysis, auto insights, filtered CSV download. |
| **EDA** | Dynamic chart builder: pick columns and chart types, with chart recommendation and validation. |
| **Prediction** | **Single prediction** via a form (with auto-fetched weather/location by district) and **bulk prediction** via CSV upload with a downloadable sample template. Returns spoilage risk class, confidence, risk level, predicted shelf life (days) and storage recommendations. Bulk results can be exported as CSV or PDF. |
| **Reports** | Prediction history stored in SQLite, with search, category filter, CSV export and clear-history. |

| **Model Performance** | Accuracy, precision, recall, F1, classification report, per-class accuracy, shelf-life regression metrics, model parameters and feature importance. |
| **Important Storage Tips** | Practical storage guidelines to reduce spoilage. |
| **About** | Project overview, objectives, algorithms and benefits. |

Also included:

- **Dataset validator**: fuzzy-matches column names in uploaded datasets to the required schema.
- **Custom model training** (`utils/train_model.py`): trains Decision Tree, Random Forest and Gradient Boosting pipelines on an uploaded dataset, picks the best by accuracy and saves it as the active model.
- **Synthetic dataset generator** (`database/dataset_generator.py`): builds 100,000 realistic Indian produce records using Faker.

---

## 🤖 Machine Learning

Two scikit-learn pipelines (preprocessing and model in one object) are trained in `post_harvest_ml_pipeline.ipynb`:

**1. Spoilage Risk Classifier** (target: `Spoilage_Risk` → Low / Medium / High)

| Metric | Value |
|---|---|
| Model | Random Forest (`n_estimators=100`, `max_depth=15`, `min_samples_split=5`) |
| Accuracy | **98.16%** |
| Precision / Recall / F1 | 98.17% / 98.16% / 98.15% |

**2. Shelf Life Regressor** (target: `Shelf_Life`, in days)

| Metric | Value |
|---|---|
| R² | 0.8039 |
| MAE | 2.23 days |
| RMSE | 2.92 days |

Training setup: 100,000 records, 80/20 split (80,000 train / 20,000 test), 31 input features.
Preprocessing: `StandardScaler` for numeric columns and `OrdinalEncoder` for categorical columns.

---

## 📁 Project Structure

```
post_harvest/
├── app.py                          # Streamlit entry point + sidebar navigation
├── post_harvest_ml_pipeline.ipynb  # End-to-end ML training notebook
├── Post_Harvest_Loss_Prevention_Report.docx   # Project report
│
├── views/                          # One file per Streamlit page
│   ├── dashboard.py  dataset.py  EDA.py  prediction.py
│   ├── reports.py  model_performance.py  storage_tips.py  about.py
│
├── utils/
│   ├── prediction.py               # Loads models; single, bulk and shelf-life prediction
│   ├── prediction_form.py          # Single-prediction input form
│   ├── recommendation.py           # Rule-based storage recommendations
│   ├── train_model.py              # Train a model from an uploaded dataset
│   ├── dataset_validator.py        # Column validation / fuzzy matching
│   └── dashboard/                  # Analytics components
│       ├── kpi.py  filters.py  statistics.py  correlation.py
│       ├── missing_analysis.py  outlier.py  insights.py
│       ├── feature_importance.py  quick_dashboard.py
│       └── chart_builder.py  chart_recommender.py  chart_renderer.py  chart_validator.py
│
├── services/
│   ├── weather_service.py          # Open-Meteo API (current weather)
│   └── location_service.py         # OpenStreetMap Nominatim (geocoding)
│
├── database/
│   ├── db.py                       # SQLite connection + table setup
│   ├── history.py                  # Save predictions to history
│   ├── dataset_generator.py        # Synthetic dataset generator (Faker)
│   └── prediction_history.db       # SQLite DB (auto-created, git-ignored)
│
├── dataset/
│   ├── Produce_Dataset.csv         # 100,000 rows × 42 columns
│   └── sample_bulk_prediction_template.csv
│
└── models/
    ├── spoilage_risk_pipeline.pkl  # Risk classifier (git-ignored)
    ├── shelf_life_pipeline.pkl     # Shelf-life regressor (git-ignored)
    ├── active_model.json           # Currently active model metadata
    ├── training_report.json        # Metrics from the last training run
    └── custom_features.json        # Feature list
```

---

## 🗂️ Dataset

`Produce_Dataset.csv` contains **100,000 records × 42 columns**, covering:

- **Produce info:** Category, Produce_Name, Variety, Produce_Grade, Quality_Score, Health_Score, Weight
- **Storage conditions:** Storage_Type, Package_Type, Storage_Duration, Temperature, Humidity, Light_Intensity, CO2_Level, Ethylene_Level, Moisture_Content
- **Supply chain:** Transport_Mode, Distance_to_Market, Cold_Chain_Available, Market_Price, Market_Demand, Storage_Cost, Farmer_ID, Warehouse_ID
- **IoT / location:** IoT_Device_ID, Sensor_Battery_Level, Sensor_Status, GPS_Latitude, GPS_Longitude, State, District
- **Environment:** Weather, Season, Disease_Detected
- **Targets / outputs:** `Spoilage_Risk`, `Shelf_Life`, Recommendation, Alert_Status

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (developed on 3.13)
- Internet connection (for weather and location lookup in the single-prediction form)

### 1. Install dependencies

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install streamlit pandas numpy scikit-learn plotly joblib requests faker fpdf2
```

### 2. Generate the trained models

`*.pkl` and `*.db` files are listed in `.gitignore`, so a fresh clone will not include them. Create them by running the notebook:

```bash
pip install jupyter
jupyter notebook post_harvest_ml_pipeline.ipynb
```

Run all cells. This saves `spoilage_risk_pipeline.pkl` and `shelf_life_pipeline.pkl` into `models/` and updates `active_model.json` and `training_report.json`.

> The app stops at start-up with a clear error if no spoilage model is found in `models/`.

### 3. (Optional) Regenerate the dataset

```bash
python database/dataset_generator.py
```

### 4. Create the history database

The Reports page reads from `database/prediction_history.db`. If the file is missing, create it once:

```bash
python -c "from database.db import initialize_database; initialize_database()"
```

### 5. Run the app

Run from the project root, because paths like `dataset/` and `database/` are relative:

```bash
streamlit run app.py
```

Then open **http://localhost:8501**.

---

## 🧭 Usage

**Single prediction**
1. Go to **Prediction → Single Prediction**.
2. Fill in produce and storage details. Weather and coordinates can be fetched from the district name.
3. Click **Run Prediction** to get the risk level, confidence, estimated shelf life and recommendations. The result is saved to history.

**Bulk prediction**
1. Go to **Prediction → Bulk Prediction**.
2. Download the sample CSV template and fill in your records.
3. Upload the CSV. Predictions run automatically.
4. Download results as CSV or PDF.

Column names are normalised automatically (case, spaces, hyphens). Missing feature columns are filled with `0`, so for reliable results provide all required features.

**Train on your own data:** `utils/train_model.py → train_uploaded_dataset(path, target_column)` trains three classifiers, saves the best as `models/custom_model.pkl` and writes the metadata to `active_model.json`.

---

## 🛠️ Tech Stack

- **Frontend / App:** Streamlit
- **ML:** scikit-learn (Random Forest, Decision Tree, Gradient Boosting), joblib
- **Data:** pandas, NumPy
- **Visualisation:** Plotly
- **Database:** SQLite
- **Reports:** FPDF2 (PDF export)
- **APIs:** Open-Meteo (weather), OpenStreetMap Nominatim (geocoding)
- **Data generation:** Faker (`en_IN` locale)

---

## ⚠️ Notes

- The dataset is **synthetically generated**, so model accuracy reflects the generated data and not real-world field performance. Validate with real data before production use.
- The app depends on external APIs (Open-Meteo, Nominatim); the single-prediction form needs internet for auto-fill.
- Model files are large (roughly 120 MB combined) and git-ignored. Share them separately or retrain with the notebook.

---

## 🎯 Objectives

Reduce post-harvest losses · predict spoilage before it occurs · improve storage management · extend shelf life · reduce food waste · support data-driven agriculture.

---

## 📄 License

Add your license here (e.g. MIT).
