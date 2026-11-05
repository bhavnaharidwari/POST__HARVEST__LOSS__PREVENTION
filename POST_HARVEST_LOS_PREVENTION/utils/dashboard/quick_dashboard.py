import streamlit as st
import plotly.express as px


# Quick Dashboard


def show_quick_dashboard(df):

    st.subheader("Quick Analytics Dashboard")

    left, right = st.columns(2)

    
    # Category Distribution
    

    with left:

        if "Category" in df.columns:

            category_df = (
                df["Category"]
                .value_counts()
                .reset_index()
            )

            category_df.columns = ["Category", "Count"]

            fig = px.bar(
                category_df,
                x="Category",
                y="Count",
                color="Category",
                text="Count",
                title="Category Distribution"
            )

            fig.update_layout(
                height=420,
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    
    # Storage Type
    

    with right:

        if "Storage_Type" in df.columns:

            storage_df = (
                df["Storage_Type"]
                .value_counts()
                .reset_index()
            )

            storage_df.columns = [
                "Storage",
                "Count"
            ]

            fig = px.pie(
                storage_df,
                names="Storage",
                values="Count",
                hole=0.55,
                title="Storage Type Distribution"
            )

            fig.update_layout(
                height=420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    left, right = st.columns(2)

    
    # Weather

    with left:

        if "Weather" in df.columns:

            weather_df = (
                df["Weather"]
                .value_counts()
                .reset_index()
            )

            weather_df.columns = [
                "Weather",
                "Count"
            ]

            fig = px.pie(
                weather_df,
                names="Weather",
                values="Count",
                title="Weather Distribution"
            )

            fig.update_layout(
                height=420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Top States
    

    with right:

        if "State" in df.columns:

            state_df = (
                df["State"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            state_df.columns = [
                "State",
                "Count"
            ]

            fig = px.bar(
                state_df,
                x="State",
                y="Count",
                color="Count",
                text="Count",
                title="Top 10 States"
            )

            fig.update_layout(
                height=420,
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()


    # Temperature Histogram
    

    if "Temperature" in df.columns:

        fig = px.histogram(
            df,
            x="Temperature",
            nbins=25,
            title="Temperature Distribution"
        )

        fig.update_layout(
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )