import os
import pandas as pd
import streamlit as st

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
# LOAD HISTORY
# --------------------------------------------------

history_file = "prediction_history.csv"

if not os.path.exists(history_file):

    st.info("No prediction history found.")
    st.stop()

history = pd.read_csv(history_file)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_predictions = len(history)

low = len(history[history["Risk Level"] == "Low"])
medium = len(history[history["Risk Level"] == "Medium"])
high = len(history[history["Risk Level"] == "High"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("📊 Total", total_predictions)
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
        "Search Date",
        placeholder="Example: 27-07-2026"
    )

filtered = history.copy()

if risk_filter != "All":
    filtered = filtered[
        filtered["Risk Level"] == risk_filter
    ]

if search:
    filtered = filtered[
        filtered["Date"].astype(str).str.contains(search)
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

latest = history.tail(5).iloc[::-1]

for _, row in latest.iterrows():

    st.write(
        f"**{row['Date']}** → "
        f"{row['Risk Level']} Risk "
        f"({row['Probability (%)']}%)"
    )

st.divider()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.download_button(
    "📥 Download History",
    history.to_csv(index=False),
    file_name="prediction_history.csv",
    mime="text/csv"
)

# --------------------------------------------------
# CLEAR HISTORY
# --------------------------------------------------

if st.button("🗑 Clear History"):

    os.remove(history_file)

    st.success("History deleted successfully.")

    st.rerun()