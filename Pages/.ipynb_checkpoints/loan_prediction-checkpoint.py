import streamlit as st
import pandas as pd
import pickle
import os
import plotly.graph_objects as go

# Database
from database.database import (
    initialize_database,
    save_prediction
)

initialize_database()

# Report Generator
from utils.report_generator import generate_report

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🏦",
    layout="wide"
)

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
# Load ML Model
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
# Title
# --------------------------------------------------

st.title("🏦 Smart Loan Risk Analytics Platform")

st.caption(
    "Predict loan default probability using Machine Learning and generate a professional assessment report."
)

st.divider()

# --------------------------------------------------
# Customer Information
# --------------------------------------------------

st.subheader("👤 Customer Information")

left, right = st.columns(2)

# ==================================================
# LEFT COLUMN
# ==================================================

with left:

    age = st.number_input(
        "Age",
        18,
        100,
        30
    )

    income = st.number_input(
        "Annual Income ($)",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    loan_amount = st.number_input(
        "Loan Amount ($)",
        min_value=0.0,
        value=10000.0,
        step=500.0
    )

    credit_score = st.slider(
        "Credit Score",
        300,
        850,
        700
    )

    months_employed = st.number_input(
        "Months Employed",
        min_value=0,
        value=60
    )

    num_credit_lines = st.number_input(
        "Number of Credit Lines",
        min_value=0,
        value=5
    )

    interest_rate = st.slider(
        "Interest Rate (%)",
        0.0,
        40.0,
        8.5
    )

    loan_term = st.selectbox(
        "Loan Term",
        [12, 24, 36, 48, 60]
    )

# ==================================================
# RIGHT COLUMN
# ==================================================

with right:

    dti_ratio = st.slider(
        "Debt-to-Income Ratio",
        0.0,
        1.0,
        0.30
    )

    education = st.selectbox(
        "Education",
        [
            "Bachelor's",
            "High School",
            "Master's",
            "PhD"
        ]
    )

    employment = st.selectbox(
        "Employment Type",
        [
            "Full-time",
            "Part-time",
            "Self-employed",
            "Unemployed"
        ]
    )

    marital = st.selectbox(
        "Marital Status",
        [
            "Divorced",
            "Married",
            "Single"
        ]
    )

    mortgage = st.selectbox(
        "Has Mortgage",
        [
            "No",
            "Yes"
        ]
    )

    dependents = st.selectbox(
        "Has Dependents",
        [
            "No",
            "Yes"
        ]
    )

    purpose = st.selectbox(
        "Loan Purpose",
        [
            "Auto",
            "Business",
            "Education",
            "Home",
            "Other"
        ]
    )

    cosigner = st.selectbox(
        "Has Co-Signer",
        [
            "No",
            "Yes"
        ]
    )

st.divider()

# --------------------------------------------------
# Encode Categorical Features
# --------------------------------------------------

education_encoded = encoders["Education"].transform([education])[0]
employment_encoded = encoders["EmploymentType"].transform([employment])[0]
marital_encoded = encoders["MaritalStatus"].transform([marital])[0]
mortgage_encoded = encoders["HasMortgage"].transform([mortgage])[0]
dependents_encoded = encoders["HasDependents"].transform([dependents])[0]
purpose_encoded = encoders["LoanPurpose"].transform([purpose])[0]
cosigner_encoded = encoders["HasCoSigner"].transform([cosigner])[0]

# --------------------------------------------------
# Input Data
# --------------------------------------------------

input_df = pd.DataFrame({

    "Age":[age],
    "Income":[income],
    "LoanAmount":[loan_amount],
    "CreditScore":[credit_score],
    "MonthsEmployed":[months_employed],
    "NumCreditLines":[num_credit_lines],
    "InterestRate":[interest_rate],
    "LoanTerm":[loan_term],
    "DTIRatio":[dti_ratio],
    "Education":[education_encoded],
    "EmploymentType":[employment_encoded],
    "MaritalStatus":[marital_encoded],
    "HasMortgage":[mortgage_encoded],
    "HasDependents":[dependents_encoded],
    "LoanPurpose":[purpose_encoded],
    "HasCoSigner":[cosigner_encoded]

})

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

        st.success("Prediction successful!")

    except Exception as e:
        st.exception(e)
        st.stop()

    # -----------------------------------------
    # Risk Analysis
    # -----------------------------------------

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

    # --------------------------------------------------
    # Save Prediction to SQLite
    # --------------------------------------------------

    prediction_id = save_prediction(

        age,

        income,

        loan_amount,

        credit_score,

        probability,

        risk_level

    )

    # --------------------------------------------------
    # Generate TXT Report
    # --------------------------------------------------

    report_path = generate_report(

        prediction_id,

        age,

        income,

        loan_amount,

        credit_score,

        probability,

        risk_level

    )

    st.divider()

    st.subheader("📊 Prediction Result")

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Prediction",

            "Default" if prediction == 1 else "No Default"

        )

    with c2:

        st.metric(

            "Default Probability",

            f"{probability*100:.2f}%"

        )

    with c3:

        st.metric(

            "Prediction ID",

            prediction_id

        )


    # --------------------------------------------------
    # Risk Dashboard
    # --------------------------------------------------
    
    st.divider()
    
    st.subheader("📊 Risk Dashboard")
    
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(probability * 100, 2),
            number={"suffix": "%"},
            title={"text": "Default Probability"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [0, 30], "color": "#22C55E"},
                    {"range": [30, 70], "color": "#FACC15"},
                    {"range": [70, 100], "color": "#EF4444"}
                ]
            }
        )
    )
    
    gauge.update_layout(height=350)
    
    st.plotly_chart(gauge, use_container_width=True)

    
    # --------------------------------------------------
    # Loan Health Score
    # --------------------------------------------------
    
    health_score = max(0, round((1 - probability) * 100))
    
    st.subheader("🏥 Loan Health Score")
    
    st.metric(
        "Overall Financial Health",
        f"{health_score}/100"
    )
    
    if health_score >= 80:
    
        st.success("Excellent financial profile.")
    
    elif health_score >= 60:
    
        st.info("Good financial profile.")
    
    elif health_score >= 40:
    
        st.warning("Moderate financial profile.")
    
    else:
    
        st.error("Poor financial profile.")
    
        st.markdown(
            f"""
    <div class="{box}">
    <h2 style="text-align:center;">
    {risk_icon} {risk_level} Risk
    </h2>
    </div>
    """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # AI Recommendation
    # --------------------------------------------------

    st.write("### 🤖 AI Recommendation")

    st.info(recommendation)

    # --------------------------------------------------
    # Download Report
    # --------------------------------------------------

    with open(report_path, "rb") as pdf:
    
        st.download_button(
    
            label="📄 Download PDF Report",
    
            data=pdf,
    
            file_name=f"{prediction_id}.pdf",
    
            mime="application/pdf",
    
            use_container_width=True
    )

    st.success("Prediction saved successfully")

    # --------------------------------------------------
    # Customer Profile
    # --------------------------------------------------

    st.divider()

    st.subheader("👤 Customer Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Personal Information")

        st.write(f"**Prediction ID:** {prediction_id}")
        st.write(f"**Age:** {age}")
        st.write(f"**Education:** {education}")
        st.write(f"**Employment:** {employment}")
        st.write(f"**Marital Status:** {marital}")
        st.write(f"**Dependents:** {dependents}")

    with col2:

        st.markdown("### Loan Information")

        st.write(f"**Annual Income:** ${income:,.2f}")
        st.write(f"**Loan Amount:** ${loan_amount:,.2f}")
        st.write(f"**Interest Rate:** {interest_rate}%")
        st.write(f"**Loan Term:** {loan_term} Months")
        st.write(f"**Credit Score:** {credit_score}")
        st.write(f"**DTI Ratio:** {dti_ratio:.2f}")

    # --------------------------------------------------
    # Financial Analysis
    # --------------------------------------------------

    st.divider()

    st.subheader("📈 Financial Analysis")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Income",
            f"${income:,.0f}"
        )

    with b:
        st.metric(
            "Loan Amount",
            f"${loan_amount:,.0f}"
        )

    with c:
        st.metric(
            "Credit Score",
            credit_score
        )

    with d:
        st.metric(
            "Interest",
            f"{interest_rate}%"
        )

    # --------------------------------------------------
    # Risk Indicators
    # --------------------------------------------------

    st.divider()

    st.subheader("🚦 Risk Indicators")

    risk_data = pd.DataFrame({

        "Indicator":[
            "Credit Score",
            "Debt-to-Income Ratio",
            "Employment Stability",
            "Mortgage",
            "Co-Signer"
        ],

        "Status":[
            credit_score,
            round(dti_ratio,2),
            employment,
            mortgage,
            cosigner
        ]

    })

    st.dataframe(
        risk_data,
        hide_index=True,
        use_container_width=True
    )

    # --------------------------------------------------
    # Customer Summary Table
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Complete Customer Summary")

    summary = pd.DataFrame({

        "Feature":[

            "Age",
            "Income",
            "Loan Amount",
            "Credit Score",
            "Months Employed",
            "Credit Lines",
            "Interest Rate",
            "Loan Term",
            "DTI Ratio",
            "Education",
            "Employment",
            "Marital Status",
            "Mortgage",
            "Dependents",
            "Loan Purpose",
            "Co-Signer"

        ],

        "Value":[

            age,
            income,
            loan_amount,
            credit_score,
            months_employed,
            num_credit_lines,
            interest_rate,
            loan_term,
            dti_ratio,
            education,
            employment,
            marital,
            mortgage,
            dependents,
            purpose,
            cosigner

        ]

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    # --------------------------------------------------
    # Approval Status
    # --------------------------------------------------
    
    st.divider()
    
    st.subheader("🏦 Loan Decision")
    
    if risk_level == "Low":
    
        st.success(
            "✅ Recommended Decision: APPROVE"
        )
    
    elif risk_level == "Medium":
    
        st.warning(
            "⚠ Recommended Decision: MANUAL REVIEW"
        )
    
    else:
    
        st.error(
            "❌ Recommended Decision: REJECT"
        )

    # --------------------------------------------------
    # AI Insights
    # --------------------------------------------------

    st.divider()

    st.subheader("🤖 AI Insights")

    insights = []

    if credit_score < 600:
        insights.append(
            "• Low credit score increases the probability of loan default."
        )

    if dti_ratio > 0.50:
        insights.append(
            "• High Debt-to-Income ratio indicates financial stress."
        )

    if months_employed < 12:
        insights.append(
            "• Short employment history increases lending risk."
        )

    if interest_rate > 20:
        insights.append(
            "• High interest rates are commonly associated with riskier borrowers."
        )

    if loan_amount > income * 0.8:
        insights.append(
            "• Loan amount is high compared to annual income."
        )

    if len(insights) == 0:
        insights.append(
            "• Customer financial profile appears stable."
        )

    for item in insights:
        st.info(item)

    # --------------------------------------------------
    # Success Message
    # --------------------------------------------------

    st.divider()

    st.success("✅ Prediction completed successfully.")

    st.caption(
        "Prediction saved to SQLite database and loan assessment report generated successfully."
    )

    st.divider()
    
    st.markdown(
        """
    <center>
    
    ### Smart Loan Risk Analytics Platform
    
    Machine Learning • Streamlit • SQLite • Plotly
    
    Developed for Loan Risk Assessment & Decision Support
    
    </center>
    """,
        unsafe_allow_html=True
    )