import streamlit as st
def apply_filters(df):

    st.subheader(" Smart Filters")

    filtered_df = df.copy()

    categorical_columns = list(
        filtered_df.select_dtypes(include="object").columns
    )

    selected_filters = {}

    with st.expander("Open Filters", expanded=False):

        for column in categorical_columns:

            values = sorted(
                filtered_df[column]
                .dropna()
                .unique()
            )

            selected = st.multiselect(
                column,
                values
            )

            if selected:

                filtered_df = filtered_df[
                    filtered_df[column].isin(selected)
                ]

                selected_filters[column] = selected

    return filtered_df, selected_filters