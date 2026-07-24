import streamlit as st
import pandas as pd
import numpy as np
import pickle

feature_importance = pd.read_csv("feature_importance.csv")

st.title("🏦Smart Loan Default Prediction")

st.set_page_config(
    page_title="Smart Loan Default Prediction",
    page_icon = "🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

model = pickle.load(open("loan_model.pkl", "rb"))
# scaler = pickle.load(open("scaler.pkl", "rb"))
encoders = pickle.load(open("encoders.pkl", "rb"))


st.markdown("""
<style>
.main{
    background-color:#F4F8FB;
}

.title{
    font-size:40px;
    font-weight:bold;
    color:#0A4D68;
}

.subtitle{
    font-size:18px;
    color:#555;
}

div[data-testid="stMetric"]{
    background-color:gray;
    border-radius:12px;
    padding:15px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<p class="title">Smart Loan Default Prediction System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Predict the probability of loan default using Machine Learning.</p>',
    unsafe_allow_html=True
)
st.divider()


st.sidebar.header("👤 Applicant Information")
age = st.sidebar.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30
)

education = st.sidebar.selectbox(
    "Education",
    encoders["Education"].classes_
)

education = encoders["Education"].transform([education])[0]

employment = st.sidebar.selectbox(
    "Employment Type",
    encoders["EmploymentType"].classes_
)

employment = encoders["EmploymentType"].transform([employment])[0]

marital = st.sidebar.selectbox(
    "Marital Status",
    encoders["MaritalStatus"].classes_
)

marital = encoders["MaritalStatus"].transform([marital])[0]

st.sidebar.header("💰 Financial Details")

income = st.sidebar.number_input(
    "Annual Income ($)",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

credit_score = st.sidebar.number_input(
    "Credit Score",
    min_value=300,
    max_value=900,
    value=650
)

months_employed = st.sidebar.number_input(
    "Months Employed",
    min_value=0,
    value=60
)

num_credit_lines = st.sidebar.number_input(
    "Number of Credit Lines",
    min_value=0,
    value=5
)

st.sidebar.header("🏦 Loan Details")

loan_amount = st.sidebar.number_input(
    "Loan Amount ($)",
    min_value=0.0,
    value=100000.0,
    step=5000.0
)

interest_rate = st.sidebar.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    value=10.5
)

loan_term = st.sidebar.number_input(
    "Loan Term (Months)",
    min_value=1,
    value=36
)

dti_ratio = st.sidebar.slider(
    "Debt-to-Income Ratio",
    min_value=0.0,
    max_value=1.0,
    value=0.30,
    step=0.01
)

mortgage = st.sidebar.selectbox(
    "Has Mortgage",
    encoders["HasMortgage"].classes_
)

mortgage = encoders["HasMortgage"].transform([mortgage])[0]

dependents = st.sidebar.selectbox(
    "Has Dependents",
    encoders["HasDependents"].classes_
)

dependents = encoders["HasDependents"].transform([dependents])[0]

purpose = st.sidebar.selectbox(
    "Loan Purpose",
    encoders["LoanPurpose"].classes_
)

purpose = encoders["LoanPurpose"].transform([purpose])[0]

cosigner = st.sidebar.selectbox(
    "Has Co-Signer",
    encoders["HasCoSigner"].classes_
)

cosigner = encoders["HasCoSigner"].transform([cosigner])[0]

predict = st.sidebar.button(
    "🔍 Predict Loan Default",
    use_container_width=True
)



st.header("📋 Customer Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Age", age)
col2.metric("Income", f"${income:,.0f}")
col3.metric("Credit Score", credit_score)
col4.metric("Loan Amount", f"${loan_amount:,.0f}")

st.divider()

if predict:
    input_data = pd.DataFrame({
        "Age":[age],
        "Income":[income],
        "LoanAmount":[loan_amount],
        "CreditScore":[credit_score],
        "MonthsEmployed":[months_employed],
        "NumCreditLines":[num_credit_lines],
        "InterestRate":[interest_rate],
        "LoanTerm":[loan_term],
        "DTIRatio":[dti_ratio],
        "Education":[education],
        "EmploymentType":[employment],
        "MaritalStatus":[marital],
        "HasMortgage":[mortgage],
        "HasDependents":[dependents],
        "LoanPurpose":[purpose],
        "HasCoSigner":[cosigner]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    st.header("📊 Prediction Result")
    
    st.metric(
        "Default Probability",
        f"{probability*100:.2f}%"
    )
    
    st.progress(float(probability))
    
    if probability < 0.30:
    
        st.success("🟢 LOW RISK")
    
    elif probability < 0.70:
    
        st.warning("🟡 MEDIUM RISK")
    
    else:
    
        st.error("🔴 HIGH RISK")
    
    if probability < 0.30:
    
        st.info(
            "Customer has a low probability of loan default."
        )
    
    elif probability < 0.70:
    
        st.info(
            "Customer has a moderate probability of loan default."
        )
    
    else:
        st.info(
            "Customer has a high probability of loan default."
        )    
        


        # ---------------- Risk Factors ----------------

    risk_factors = []
    
    if credit_score < 600:
        risk_factors.append(f"❌ Very Low Credit Score ({credit_score})")
    
    if income < 300000:
        risk_factors.append(f"❌ Low Annual Income (${income:,})")
    
    if loan_amount > 2000000:
        risk_factors.append(f"❌ Very High Loan Amount (${loan_amount:,})")
    
    if dti_ratio > 0.50:
        risk_factors.append(f"❌ High Debt-to-Income Ratio ({dti_ratio:.2f})")
    
    if months_employed < 12:
        risk_factors.append(f"❌ Short Employment History ({months_employed} months)")
    
    if interest_rate > 18:
        risk_factors.append(f"❌ High Interest Rate ({interest_rate}%)")

    st.subheader("⚠ Risk Factors")

    if risk_factors:
        for factor in risk_factors:
            st.write(factor)
    else:
        st.success("✅ No major risk factors detected.")    

        # ---------------- Smart Recommendation ----------------

    st.subheader("💡 Loan Recommendation")
    
    if probability < 0.30:
        risk_level = "Low Risk"
        recommendation = "Loan Approval Recommended"
    
        st.success("✅ Loan Approval Recommended")
        st.write("""
    The customer has a **low chance of defaulting** on the loan.
    
    **Why?**
    - Good financial profile
    - Low overall risk
    - Loan can be approved with the normal verification process.
    """)
    
    elif probability < 0.70:
        risk_level = "Medium Risk"
        recommendation = "Manual Verification Recommended"
    
        st.warning("🟡 Manual Verification Recommended")
        st.write("""
    The customer has a **moderate risk of default**.
    
    **Suggested Action:**
    - Verify income documents
    - Check employment details
    - Review credit history before making the final decision.
    """)
    
    else:
        risk_level = "High Risk"
        recommendation = "Loan Rejection Recommended"
    
        st.error("❌ Loan Rejection Recommended")
        st.write("""
    The customer has a **high chance of defaulting** on the loan.
    
    **Suggested Action:**
    - Avoid approving the loan in the current condition.
    - Ask the customer to improve their credit score or financial profile before applying again.
    """)

    st.subheader("📊 Feature Importance")
    feature_importance = pd.read_csv("feature_importance.csv")
    
    st.bar_chart(
        feature_importance.set_index("Feature")
    )
    

    st.subheader("📄 Download Prediction Report")

    report = pd.DataFrame({
        "Field": [
            "Age",
            "Income",
            "Credit Score",
            "Loan Amount",
            "Default Probability",
            "Risk Level",
            "Recommendation"
        ],
        "Value": [
            age,
            income,
            credit_score,
            loan_amount,
            f"{probability*100:.2f}%",
            risk_level,
            recommendation
        ]
    })

    csv = report.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="loan_prediction_report.csv",
        mime="text/csv"
    )
