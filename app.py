import streamlit as st
from database.database import initialize_database

st.set_page_config(
    page_title="Smart Loan Risk Analytics Platform",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] > div:first-child {
    display: none;
}
</style>
""", unsafe_allow_html=True)

initialize_database()

dashboard = st.Page("Pages/dashboard.py", title="Dashboard", icon="🏠")
loan = st.Page("Pages/loan_prediction.py", title="Loan Prediction", icon="🤖")
history = st.Page("Pages/prediction_history.py", title="Prediction History", icon="📜")
insights = st.Page("Pages/model.py", title="Model Insights", icon="📈")

pg = st.navigation([dashboard, loan, history, insights])
pg.run()