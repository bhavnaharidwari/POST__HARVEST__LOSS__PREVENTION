import streamlit as st
def storage_tips_page():

    st.title("Important Storage Tips")

    st.markdown(
        """
        Practical storage guidelines to reduce post-harvest spoilage
        and maintain produce quality.
        """
    )

    st.divider()

    tips = [
        "Store apples at 0–4°C for longer shelf life.",
        "Keep mangoes away from direct sunlight.",
        "Maintain humidity between 85–95% for vegetables.",
        "Avoid storing tomatoes below 10°C.",
        "Use cold chain transportation whenever possible.",
        "Keep storage area clean and well ventilated.",
        "Regularly monitor temperature and humidity sensors.",
        "Remove spoiled produce immediately to prevent contamination."
    ]

    for tip in tips:

        with st.container(border=True):

            st.write(tip)

    st.divider()