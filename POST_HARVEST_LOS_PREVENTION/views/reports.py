import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path("database") / "prediction_history.db"


def reports_page():

    st.title(" Prediction History")


    # Load Data


    try:

        conn = sqlite3.connect(DB_PATH)

        df = pd.read_sql_query(
            """
            SELECT *
            FROM prediction_history
            ORDER BY id DESC
            """,
            conn
        )

        conn.close()

    except Exception as e:

        st.error(f"Database Error: {e}")
        return


    # Empty Database


    if df.empty:

        st.info("No prediction history found.")

        return

    # Search


    search = st.text_input(
        " Search Produce"
    )

    if search:

        df = df[
            df["produce_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    # Category Filter


    category = st.selectbox(

        "Category",

        ["All"] + sorted(
            df["category"]
            .unique()
            .tolist()
        )

    )

    if category != "All":

        df = df[
            df["category"] == category
        ]

    st.divider()

    # Table

    st.subheader("Prediction Records")

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # Download CSV
    

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        " Download CSV",

        csv,

        "prediction_history.csv",

        "text/csv",

        use_container_width=True

    )

    st.divider()


    # Clear History


    if st.button(
        "🗑 Clear History",
        use_container_width=True
    ):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM prediction_history"
        )

        conn.commit()

        conn.close()

        st.success(
            "Prediction history cleared successfully."
        )

        st.rerun()