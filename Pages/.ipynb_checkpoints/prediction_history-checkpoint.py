import streamlit as st
import pandas as pd

from database.database import get_history, clear_history

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📜 Prediction History")
st.caption("View and manage all previous loan risk predictions.")

st.divider()

# --------------------------------------------------
# LOAD DATA FROM SQLITE
# --------------------------------------------------

rows = get_history()

if len(rows) == 0:
    st.info("No prediction history found.")
    st.stop()

history = pd.DataFrame(
    rows,
    columns=[
        "ID",
        "Prediction ID",
        "Date",
        "Age",
        "Income",
        "Loan Amount",
        "Credit Score",
        "Probability (%)",
        "Risk Level"
    ]
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_predictions = len(history)

low = len(history[history["Risk Level"] == "Low"])
medium = len(history[history["Risk Level"] == "Medium"])
high = len(history[history["Risk Level"] == "High"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("📊 Total Predictions", total_predictions)
c2.metric("🟢 Low Risk", low)
c3.metric("🟡 Medium Risk", medium)
c4.metric("🔴 High Risk", high)

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

left, right = st.columns(2)

with left:
    risk_filter = st.selectbox(
        "Filter by Risk Level",
        ["All", "Low", "Medium", "High"]
    )

with right:
    search = st.text_input(
        "Search by Date",
        placeholder="Example: 28-07-2026"
    )

filtered = history.copy()

if risk_filter != "All":
    filtered = filtered[
        filtered["Risk Level"] == risk_filter
    ]

if search:
    filtered = filtered[
        filtered["Date"].astype(str).str.contains(search, case=False)
    ]

# --------------------------------------------------
# HISTORY TABLE
# --------------------------------------------------

st.subheader("📋 Prediction Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.divider()

# --------------------------------------------------
# RECENT ACTIVITY
# --------------------------------------------------

st.subheader("🕒 Recent Activity")

latest = history.head(5)

for _, row in latest.iterrows():

    st.write(
        f"**{row['Date']}** → "
        f"**{row['Risk Level']} Risk** "
        f"({row['Probability (%)']}%)"
    )

st.divider()

# --------------------------------------------------
# DOWNLOAD CSV
# --------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download History",
    csv,
    file_name="prediction_history.csv",
    mime="text/csv"
)

st.divider()

# --------------------------------------------------
# CLEAR HISTORY
# --------------------------------------------------

if st.button("🗑 Clear History", use_container_width=True):

    clear_history()

    st.success("Prediction history cleared successfully.")

    st.rerun()