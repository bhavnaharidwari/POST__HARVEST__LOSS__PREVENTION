from difflib import SequenceMatcher


class DatasetValidator:

    def __init__(self):

        
        # Required Columns
        

        self.required_columns = {

            "Category": [
                "category",
                "type",
                "produce_category"
            ],

            "Produce_Name": [
                "produce_name",
                "produce",
                "fruit",
                "vegetable",
                "crop",
                "item"
            ],

            "Temperature": [
                "temperature",
                "temp",
                "temp_c",
                "storage_temperature"
            ],

            "Humidity": [
                "humidity",
                "rh",
                "relative_humidity"
            ],

            "Storage_Type": [
                "storage_type",
                "storage",
                "warehouse",
                "cold_storage"
            ],

            "Storage_Duration": [
                "storage_duration",
                "days",
                "duration",
                "days_in_storage"
            ],

            "Weather": [
                "weather",
                "climate"
            ],

            "Season": [
                "season"
            ],

            "Quality_Score": [
                "quality_score",
                "quality"
            ],

            "Health_Score": [
                "health_score",
                "health"
            ],

            "CO2_Level": [
                "co2",
                "co2_level"
            ],

            "Ethylene_Level": [
                "ethylene",
                "ethylene_level"
            ]
        }

        
        # Target Column
        

        self.target_columns = [

            "spoilage_status",
            "spoilage",
            "status",
            "target",
            "label",
            "prediction",
            "freshness",
            "risk"

        ]

    
    # Similarity


    def similarity(self, a, b):

        return SequenceMatcher(
            None,
            a.lower(),
            b.lower()
        ).ratio()
        
    # Validate Dataset
    

    def validate_dataset(self, df):

        result = {

            "score": 0,

            "status": "Rejected",

            "matched_columns": {},

            "missing_columns": [],

            "found_target": None,

            "warnings": [],

            "rows": len(df),

            "columns": len(df.columns)

        }

        score = 0

        uploaded_columns = [
            str(col).strip().lower()
            for col in df.columns
        ]

        # ------------------------------------------------------
        # Target Column Check (40 Marks)
        # ------------------------------------------------------

        for col in uploaded_columns:

            if col in self.target_columns:

                result["found_target"] = col

                score += 40

                break

        if result["found_target"] is None:

            result["warnings"].append(
                "Target column not found."
            )

        # ------------------------------------------------------
        # Feature Matching (40 Marks)
        # ------------------------------------------------------

        feature_marks = {

            "Category": 3,
            "Produce_Name": 5,
            "Temperature": 5,
            "Humidity": 5,
            "Storage_Type": 4,
            "Storage_Duration": 4,
            "Weather": 3,
            "Season": 3,
            "Quality_Score": 3,
            "Health_Score": 3,
            "CO2_Level": 1,
            "Ethylene_Level": 1

        }

        for feature, aliases in self.required_columns.items():

            found = False

            for uploaded in uploaded_columns:

                for alias in aliases:

                    similarity = self.similarity(
                        uploaded,
                        alias
                    )

                    if similarity >= 0.80:

                        result["matched_columns"][feature] = uploaded

                        score += feature_marks.get(feature, 0)

                        found = True

                        break

                if found:
                    break

            if not found:

                result["missing_columns"].append(feature)

        # ------------------------------------------------------
        # Dataset Size (10 Marks)
        # ------------------------------------------------------

        if len(df) >= 1000:

            score += 10

        elif len(df) >= 300:

            score += 8

        elif len(df) >= 100:

            score += 6

        elif len(df) >= 50:

            score += 4

        else:

            result["warnings"].append(
                "Very small dataset."
            )

        # ------------------------------------------------------
        # Dataset Quality (10 Marks)
        # ------------------------------------------------------

        missing_percent = (
            df.isnull().sum().sum()
            /
            (df.shape[0] * df.shape[1])
        ) * 100

        if missing_percent <= 5:

            score += 10

        elif missing_percent <= 15:

            score += 7

        elif missing_percent <= 25:

            score += 5

        else:

            result["warnings"].append(
                "Too many missing values."
            )

        # ------------------------------------------------------
        # Final Score
        # ------------------------------------------------------

        result["score"] = round(score, 2)

        if score >= 85:

            result["status"] = "Excellent"

        elif score >= 70:

            result["status"] = "Accepted"

        elif score >= 50:

            result["status"] = "Accepted with Warning"

        else:

            result["status"] = "Rejected"

        return result