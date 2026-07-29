import streamlit as st
import pandas as pd
import pickle
import os
import plotly.graph_objects as go

from database.database import save_prediction
from utils.report_generator import generate_report


# --------------------------------------------------
# Load CSS
# --------------------------------------------------

def load_css():
    if os.path.exists("assets/style.css"):
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()


# --------------------------------------------------
# Load Model & Encoders
# --------------------------------------------------

@st.cache_resource
def load_files():

    with open("loan_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("encoders.pkl", "rb") as f:
        encoders = pickle.load(f)

    return model, encoders


model, encoders = load_files()


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "probability" not in st.session_state:
    st.session_state.probability = None

if "prediction_id" not in st.session_state:
    st.session_state.prediction_id = None

if "risk_level" not in st.session_state:
    st.session_state.risk_level = None

if "report_path" not in st.session_state:
    st.session_state.report_path = None


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🏦 Smart Loan Risk Analytics Platform")

st.caption(
    "Predict loan default probability using Machine Learning and generate a professional assessment report."
)

st.divider()

# --------------------------------------------------
# Predict Button
# --------------------------------------------------

predict_btn = st.button(
    "🔍 Predict Loan Default",
    use_container_width=True,
    type="primary"
)

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if predict_btn:

    try:

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        if probability < 0.30:

            risk_level = "Low"
            risk_icon = "🟢"
            box = "result-success"

            recommendation = """
✅ Loan Approval Recommended

• Customer has a very low probability of default.

• Credit profile is healthy.

• Loan can be approved after standard verification.
"""

        elif probability < 0.70:

            risk_level = "Medium"
            risk_icon = "🟡"
            box = "result-warning"

            recommendation = """
⚠ Manual Verification Recommended

• Moderate probability of default.

• Verify income documents.

• Review employment history.

• Check credit report before approval.
"""

        else:

            risk_level = "High"
            risk_icon = "🔴"
            box = "result-danger"

            recommendation = """
❌ Loan Rejection Recommended

• High probability of default.

• Financial profile needs improvement.

• Consider reducing loan amount.

• Recommend adding a co-signer.
"""

        prediction_id = save_prediction(
            age,
            income,
            loan_amount,
            credit_score,
            probability,
            risk_level
        )

        report_path = generate_report(
            prediction_id,
            age,
            income,
            loan_amount,
            credit_score,
            probability,
            risk_level
        )

        # -----------------------------
        # Save Everything in Session
        # -----------------------------

        st.session_state.prediction_done = True

        st.session_state.prediction = prediction

        st.session_state.probability = probability

        st.session_state.prediction_id = prediction_id

        st.session_state.risk_level = risk_level

        st.session_state.report_path = report_path

        st.session_state.recommendation = recommendation

        st.session_state.risk_icon = risk_icon

        st.session_state.box = box

        st.success("Prediction Successful!")

    except Exception as e:

        st.exception(e)


    # --------------------------------------------------
    # Show Previous Prediction
    # --------------------------------------------------
    
    if st.session_state.prediction_done:
    
        prediction = st.session_state.prediction
    
        probability = st.session_state.probability
    
        prediction_id = st.session_state.prediction_id
    
        risk_level = st.session_state.risk_level
    
        report_path = st.session_state.report_path
    
        recommendation = st.session_state.recommendation
    
        risk_icon = st.session_state.risk_icon
    
        box = st.session_state.box


    # --------------------------------------------------
    # Display Result
    # --------------------------------------------------
    
    if st.session_state.prediction_done:
    
        probability = st.session_state.probability
        risk_level = st.session_state.risk_level
        prediction_id = st.session_state.prediction_id
        recommendation = st.session_state.recommendation
        risk_icon = st.session_state.risk_icon
        box = st.session_state.box
    
        st.divider()
    
        st.subheader("📊 Prediction Result")
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.metric(
                "Prediction ID",
                prediction_id
            )
    
        with col2:
            st.metric(
                "Risk Level",
                risk_level
            )
    
        with col3:
            st.metric(
                "Default Probability",
                f"{probability*100:.2f}%"
            )

    # --------------------------------------------------
    # Risk Summary
    # --------------------------------------------------
    
    st.markdown(
        f"""
    <div class="{box}">
    <h3>{risk_icon} {risk_level} Risk</h3>
    
    <p>
    Estimated Default Probability :
    <b>{probability*100:.2f}%</b>
    </p>
    
    </div>
    """,
    unsafe_allow_html=True
    )

    st.info(recommendation)

    # --------------------------------------------------
    # Health Score
    # --------------------------------------------------
    
    health_score = round((1-probability)*100)
    
    st.progress(
        health_score/100
    )
    
    st.success(
        f"Customer Financial Health Score : {health_score}/100"
    )


    if probability < 0.30:
    
        st.success("Loan is likely to be approved.")
    
    elif probability < 0.70:
    
        st.warning("Loan requires manual verification.")
    
    else:
    
        st.error("High default risk detected.")


    # --------------------------------------------------
    # Customer Summary
    # --------------------------------------------------
    
    st.divider()
    st.subheader("👤 Customer Summary")
    
    summary_df = pd.DataFrame({
        "Field": [
            "Age",
            "Annual Income",
            "Loan Amount",
            "Credit Score",
            "Risk Level",
            "Default Probability"
        ],
    
        "Value": [
            age,
            f"${income:,.2f}",
            f"${loan_amount:,.2f}",
            credit_score,
            risk_level,
            f"{probability*100:.2f}%"
        ]
    })
    
    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # Financial Analysis
    # --------------------------------------------------
    
    st.subheader("💰 Financial Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
    
        st.metric(
            "Annual Income",
            f"${income:,.2f}"
        )
    
        st.metric(
            "Loan Amount",
            f"${loan_amount:,.2f}"
        )
    
    with col2:
    
        debt_ratio = loan_amount / income
    
        st.metric(
            "Debt Ratio",
            f"{debt_ratio:.2f}"
        )
    
        st.metric(
            "Credit Score",
            credit_score
        )


        risk_table = pd.DataFrame({

    "Metric":[

        "Default Probability",
        "Risk Level",
        "Financial Health Score",
        "Debt Ratio"

    ],

    "Value":[

        f"{probability*100:.2f}%",
        risk_level,
        f"{health_score}/100",
        f"{debt_ratio:.2f}"

    ]
    })
    
    st.subheader("📈 Risk Analysis")
    
    st.table(risk_table)

    # --------------------------------------------------
    # Download Report
    # --------------------------------------------------
    
    st.subheader("📄 Download Report")
    
    if report_path and os.path.exists(report_path):
    
        with open(report_path, "rb") as pdf:
    
            st.download_button(
    
                label="⬇ Download Loan Assessment Report",
    
                data=pdf,
    
                file_name=os.path.basename(report_path),
    
                mime="application/pdf",
    
                use_container_width=True
    
            )
            

    st.divider()

    if st.button(
        "🔄 New Prediction",
        use_container_width=True
    ):
    
        keys = [
            "prediction_done",
            "prediction",
            "probability",
            "prediction_id",
            "risk_level",
            "report_path",
            "recommendation",
            "risk_icon",
            "box"
        ]
    
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
    
        st.rerun()

    # --------------------------------------------------
    # AI Insights
    # --------------------------------------------------
    
    st.divider()
    
    st.subheader("🤖 AI Risk Insights")
    
    insights = []
    
    if credit_score < 600:
        insights.append("• Low credit score increases the probability of default.")
    
    elif credit_score > 750:
        insights.append("• Excellent credit score reduces loan default risk.")
    
    if loan_amount > income * 0.5:
        insights.append("• Requested loan amount is relatively high compared to annual income.")
    
    else:
        insights.append("• Loan amount appears reasonable compared to annual income.")
    
    if age < 25:
        insights.append("• Younger applicants generally have limited credit history.")
    
    elif age > 55:
        insights.append("• Applicant has mature financial profile.")
    
    if probability > 0.70:
        insights.append("• Machine Learning model detected multiple high-risk indicators.")
    
    elif probability > 0.30:
        insights.append("• Model suggests moderate financial risk.")
    
    else:
        insights.append("• Model found strong indicators of repayment capability.")
    
    for point in insights:
        st.write(point)


    # --------------------------------------------------
    # Final Decision
    # --------------------------------------------------
    
    st.divider()
    
    st.subheader("🏦 Final Recommendation")
    
    if probability < 0.30:
    
        st.success("""
    ### ✅ APPROVE LOAN
    
    The applicant has a low probability of default.
    
    Recommendation:
    - Standard Verification
    - Normal Interest Rate
    - Eligible for Loan
    """)
    
    elif probability < 0.70:
    
        st.warning("""
    ### ⚠ MANUAL REVIEW
    
    The applicant falls into the medium-risk category.
    
    Recommendation:
    - Verify Income
    - Verify Employment
    - Check Bank Statements
    - Consider Lower Loan Amount
    """)
    
    else:
    
        st.error("""
    ### ❌ HIGH RISK
    
    The applicant has a high probability of default.
    
    Recommendation:
    - Reject Loan
    OR
    - Ask for Guarantor
    OR
    - Reduce Loan Amount
    """)

    st.divider()

    st.caption(
        "Smart Loan Risk Analytics Platform | Built using Streamlit, Scikit-Learn and Machine Learning"
    )