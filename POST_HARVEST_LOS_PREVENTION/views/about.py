import streamlit as st


def about_page():

    st.title("About Project")

    st.markdown("---")

    
    # Project Overview
    

    st.header("Project Overview")

    st.write("""
The **Post-Harvest Loss Prevention System** is an Artificial Intelligence powered
decision support system developed to reduce post-harvest losses in fruits and
vegetables.

The system predicts spoilage risk using Machine Learning models based on
environmental conditions, storage information, produce characteristics and
quality parameters.

It helps farmers, warehouse managers, distributors and food industries monitor
storage conditions, estimate remaining shelf life and take preventive actions
before spoilage occurs.

The application also provides dataset analytics, interactive visualization,
prediction history and intelligent recommendations to improve storage quality
and reduce food waste.
""")

    st.markdown("---")

    
    # Key Features


    st.header("Key Features")

    feature1, feature2 = st.columns(2)

    with feature1:

        st.subheader("Dataset Analytics")

        st.write("""
- Dataset Preview
- Smart Filters
- KPI Dashboard
- Statistical Analysis
- Correlation Analysis
- Missing Value Analysis
- Outlier Detection
- Interactive Charts
- Dataset Insights
""")

        st.subheader("Prediction")

        st.write("""
- Spoilage Prediction
- Confidence Score
- Risk Analysis
- Shelf Life Estimation
- Storage Recommendations
""")

    with feature2:

        st.subheader("Analytics")

        st.write("""
- Interactive Data Analysis
- Statistical Analysis
- Correlation Analysis
- Outlier Detection
""")

        st.subheader("Visualization")

        st.write("""
- Plotly Charts
- Interactive Dashboard
- Data Visualization
- Analytics Reports
""")

    st.markdown("---")

    
    # Project Objectives
    

    st.header("Project Objectives")

    objectives = [
        "Reduce post-harvest losses",
        "Predict spoilage before it occurs",
        "Improve storage management",
        "Increase shelf life of produce",
        "Reduce food waste",
        "Support farmers and warehouse managers",
        "Improve supply chain efficiency",
        "Provide AI-based decision support",
        "Provide smart storage recommendations",
        "Support data-driven agriculture"
    ]

    for item in objectives:
        st.write(f"• {item}")

    st.markdown("---")

    
    # Algorithms Used
    

    st.header("Machine Learning Algorithms")

    st.write("""
The project uses multiple Machine Learning classification algorithms.
Their performance can be compared to identify a suitable model for
spoilage prediction.
""")

    algorithm_data = {
        "Algorithm": [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "XGBoost",
            "LightGBM",
            "CatBoost"
        ],
        "Purpose": [
            "Baseline Classification",
            "Tree Based Classification",
            "Prediction Model",
            "Performance Comparison",
            "Gradient Boosting",
            "Categorical Feature Learning"
        ]
    }

    st.table(algorithm_data)

    st.text(
        "Final Selected Model: Random Forest Classifier"
    )

    st.markdown("---")

    
    # Benefits
    

    st.header("Benefits of the System")

    benefits = [

        "Reduces post-harvest losses",

        "Improves storage quality",

        "Minimizes food waste",

        "Supports warehouse management",

        "Helps farmers take better decisions",

        "Provides AI-based recommendations",

        "Improves supply chain efficiency",

        "Increases shelf life",

        "Easy to use interface",

        "Fast and accurate predictions",

        "Supports data-driven agriculture",

        "Helps reduce storage and transportation losses"

    ]

    for item in benefits:

        st.write(f"• {item}")

    st.markdown("---")
