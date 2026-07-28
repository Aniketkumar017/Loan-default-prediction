import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD CSS ---------------- #

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("Loan_default.csv")
feature_df = pd.read_csv("feature_importance.csv")

# ---------------- TITLE ---------------- #

st.title("📊 Banking Analytics Dashboard")
st.write("Monitor dataset statistics and model insights.")

st.divider()

# =====================================================
# KPI CARDS
# =====================================================

total_records = len(df)
total_features = len(df.columns) - 1

# Change according to your trained model
model_accuracy = 91.3

default_rate = 0

if "Default" in df.columns:
    default_rate = round(df["Default"].mean() * 100, 2)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="📁 Total Records",
        value=f"{total_records:,}"
    )

with c2:
    st.metric(
        label="📌 Features",
        value=total_features
    )

with c3:
    st.metric(
        label="🎯 Model Accuracy",
        value=f"{model_accuracy}%"
    )

with c4:
    st.metric(
        label="⚠ Default Rate",
        value=f"{default_rate}%"
    )

st.divider()

# =====================================================
# ROW 1
# =====================================================

left, right = st.columns(2)

# ---------- Loan Distribution ---------- #

with left:

    st.subheader("🥧 Loan Default Distribution")

    if "Default" in df.columns:

        counts = df["Default"].value_counts().reset_index()
        counts.columns = ["Status", "Count"]

        counts["Status"] = counts["Status"].replace({
            0: "No Default",
            1: "Default"
        })

        fig = px.pie(
            counts,
            names="Status",
            values="Count",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------- Credit Score ---------- #

with right:

    st.subheader("📉 Credit Score Distribution")

    if "CreditScore" in df.columns:

        fig = px.histogram(
            df,
            x="CreditScore",
            nbins=30
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# ROW 2
# =====================================================

left, right = st.columns(2)

# ---------- Income ---------- #

with left:

    if "Income" in df.columns:

        st.subheader("💰 Income Distribution")

        fig = px.histogram(
            df,
            x="Income",
            nbins=25
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------- Loan Amount ---------- #

with right:

    if "LoanAmount" in df.columns:

        st.subheader("🏦 Loan Amount Distribution")

        fig = px.histogram(
            df,
            x="LoanAmount",
            nbins=25
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

st.subheader("📈 Feature Importance")

feature_df = feature_df.sort_values(
    by="Importance",
    ascending=True
)

fig = px.bar(
    feature_df,
    x="Importance",
    y="Feature",
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# NUMERICAL SUMMARY
# =====================================================

st.subheader("📊 Numerical Summary")

st.dataframe(
    df.describe(),
    use_container_width=True
)

st.divider()

# =====================================================
# DATASET PREVIEW
# =====================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(15),
    use_container_width=True
)

st.divider()

# =====================================================
# MODEL INFORMATION
# =====================================================

st.subheader("🤖 Model Information")

col1, col2 = st.columns(2)

with col1:

    st.success("""
**Algorithm Used**

- Random Forest Classifier

- Supervised Machine Learning

- Binary Classification
""")

with col2:

    st.info("""
**Prediction Output**

✔ Loan Approval Recommendation

✔ Default Probability

✔ Risk Level

✔ Downloadable Report
""")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">

<b>🏦 Smart Loan Default Prediction System</b><br>

Developed using Python, Streamlit, Scikit-Learn & Plotly

</div>
""", unsafe_allow_html=True)