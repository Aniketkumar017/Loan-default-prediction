import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Model Insights",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Load CSS
# --------------------------------------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --------------------------------------------------
# Load Feature Importance
# --------------------------------------------------

feature_df = pd.read_csv("feature_importance.csv")

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🤖 Model Insights")

st.write(
    "Understand how the Random Forest model predicts loan default."
)

st.divider()

# ==================================================
# MODEL OVERVIEW
# ==================================================

st.subheader("📌 Model Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Algorithm", "Random Forest")

with c2:
    st.metric("Problem Type", "Classification")

with c3:
    st.metric("Output", "Default / No Default")

st.divider()

# ==================================================
# WHY RANDOM FOREST
# ==================================================

st.subheader("🌲 Why Random Forest?")

st.success("""

Random Forest was selected because:

✔ High prediction accuracy

✔ Handles both numerical and categorical features

✔ Reduces overfitting

✔ Works well on large datasets

✔ Provides Feature Importance

✔ Robust against noisy data

""")

st.divider()

# ==================================================
# MODEL WORKFLOW
# ==================================================

st.subheader("⚙ Model Workflow")

st.markdown("""

```text
Customer Data

        │

        ▼

Data Cleaning

        │

        ▼

Label Encoding

        │

        ▼

Random Forest Model

        │

        ▼

Prediction

        │

        ▼

Probability Score

        │

        ▼

Risk Level

        │

        ▼

Recommendation """)
