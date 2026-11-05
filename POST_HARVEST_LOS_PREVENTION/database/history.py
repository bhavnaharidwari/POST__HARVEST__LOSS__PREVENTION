import sqlite3
from pathlib import Path
from datetime import datetime

# Database Path

DB_PATH = Path("database") / "prediction_history.db"

# Save Prediction

def save_prediction(
    produce_name,
    category,
    prediction,
    confidence,
    risk_level,
    model_type="Default Model",
    model_name="Default Random Forest Model",
    model_accuracy=None
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    
    # Check Existing Columns
    

    cursor.execute(
        "PRAGMA table_info(prediction_history)"
    )

    existing_columns = [
        row[1]
        for row in cursor.fetchall()
    ]


    # Add Model Columns If Missing
    

    if "model_type" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE prediction_history
            ADD COLUMN model_type TEXT
            """
        )

    if "model_name" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE prediction_history
            ADD COLUMN model_name TEXT
            """
        )

    if "model_accuracy" not in existing_columns:

        cursor.execute(
            """
            ALTER TABLE prediction_history
            ADD COLUMN model_accuracy REAL
            """
        )

    
    # Insert Prediction
    

    cursor.execute(
        """
        INSERT INTO prediction_history (

            prediction_time,
            produce_name,
            category,
            prediction,
            confidence,
            risk_level,
            model_type,
            model_name,
            model_accuracy

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

            produce_name,

            category,

            str(prediction),

            float(confidence),

            risk_level,

            model_type,

            model_name,

            (
                float(model_accuracy)
                if model_accuracy is not None
                else None
            )
        )
    )

    conn.commit()

    conn.close()