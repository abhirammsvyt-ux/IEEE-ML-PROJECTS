import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load("models/diabetes_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🩺 Project Information")

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=True
    )

    st.divider()

    st.success("Model Accuracy: 76.62%")

    st.info("""
IEEE AI/ML Internship Project

Dataset:
Pima Indians Diabetes Dataset

Algorithm:
Logistic Regression
""")

    st.divider()

    st.caption(
        "Developed using Streamlit & Scikit-Learn"
    )

# --------------------------------------------------
# THEME
# --------------------------------------------------

if dark_mode:
    bg_color = "#0E1117"
    card_color = "#1E1E1E"
    text_color = "#FFFFFF"
else:
    bg_color = "#F5F7FA"
    card_color = "#FFFFFF"
    text_color = "#000000"

st.markdown(
    f"""
<style>

.stApp {{
    background-color: {bg_color};
    color: {text_color};
}}

.main-header {{
    background: linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}}

.metric-card {{
    background-color: {card_color};
    padding: 20px;
    border-radius: 15px;
    text-align:center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
}}

</style>
""",
    unsafe_allow_html=True
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="main-header">
<h1>🩺 Diabetes Risk Prediction System</h1>
<h4>AI Powered Healthcare Screening Tool</h4>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MEDICAL BANNER
# --------------------------------------------------

st.image(
    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?auto=format&fit=crop&w=1400&q=80",
    use_container_width=True
)

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📋 Patient Information")

    pregnancies = st.number_input(
        "Number of Pregnancies",
        min_value=0,
        value=0
    )

    glucose = st.number_input(
        "Glucose Level",
        min_value=0,
        value=120
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=0,
        value=70
    )

    skin_thickness = st.number_input(
        "Skin Thickness",
        min_value=0,
        value=20
    )

    insulin = st.number_input(
        "Insulin Level",
        min_value=0,
        value=80
    )

with col2:

    st.subheader("❤️ Health Metrics")

    bmi = st.number_input(
        "BMI",
        min_value=0.0,
        value=25.0
    )

    dpf = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        value=0.5,
        format="%.3f"
    )

    age = st.number_input(
        "Age",
        min_value=1,
        value=30
    )

# --------------------------------------------------
# HEALTH SUMMARY
# --------------------------------------------------

st.subheader("📊 Health Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Glucose", glucose)

with c2:
    st.metric("BMI", bmi)

with c3:
    st.metric("Age", age)

with c4:
    st.metric("Blood Pressure", blood_pressure)

# --------------------------------------------------
# BMI CATEGORY
# --------------------------------------------------

st.subheader("❤️ BMI Category")

if bmi < 18.5:
    st.info("Underweight")
elif bmi < 25:
    st.success("Normal Weight")
elif bmi < 30:
    st.warning("Overweight")
else:
    st.error("Obese")

# --------------------------------------------------
# BUTTON
# --------------------------------------------------

predict = st.button(
    "🔍 Analyze Diabetes Risk",
    use_container_width=True
)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if predict:

    input_df = pd.DataFrame(
        [[
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            dpf,
            age
        ]],
        columns=[
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ]
    )

    input_scaled = scaler.transform(input_df)

    prediction = model.predict(
        input_scaled
    )[0]

    probability = model.predict_proba(
        input_scaled
    )[0][1]

    st.divider()

    st.subheader("📈 Prediction Result")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Diabetes Probability",
            f"{probability*100:.2f}%"
        )

    with c2:
        st.metric(
            "Model Used",
            "Logistic Regression"
        )

    # Risk Meter

    st.subheader("🎯 Risk Meter")

    st.progress(float(probability))

    st.metric(
        "Risk Percentage",
        f"{probability*100:.2f}%"
    )

    # Risk Status

    if probability >= 0.70:
        st.error(
            f"🔴 HIGH RISK OF DIABETES ({probability*100:.2f}%)"
        )

    elif probability >= 0.40:
        st.warning(
            f"🟠 MODERATE RISK OF DIABETES ({probability*100:.2f}%)"
        )

    else:
        st.success(
            f"🟢 LOW RISK OF DIABETES ({probability*100:.2f}%)"
        )

    # Dashboard

    st.subheader("🩺 Patient Risk Dashboard")

    dashboard = pd.DataFrame({
        "Parameter": [
            "Glucose",
            "Blood Pressure",
            "BMI",
            "Age"
        ],
        "Value": [
            glucose,
            blood_pressure,
            bmi,
            age
        ]
    })

    st.dataframe(
        dashboard,
        use_container_width=True
    )

    # Recommendations

    with st.expander(
        "💡 View Health Recommendations",
        expanded=True
    ):

        if prediction == 1:

            st.markdown("""
### Recommended Actions

✅ Consult a healthcare professional

✅ Monitor blood glucose levels regularly

✅ Follow a balanced diet

✅ Exercise regularly

✅ Maintain a healthy BMI

✅ Schedule periodic health checkups
""")

        else:

            st.markdown("""
### Recommended Actions

✅ Continue healthy lifestyle habits

✅ Maintain regular exercise

✅ Eat a balanced diet

✅ Monitor health parameters

✅ Stay hydrated

✅ Attend routine medical checkups
""")

    # Factors

    with st.expander(
        "🔍 Factors Considered by the Model"
    ):

        st.markdown("""
### Input Features

• Pregnancies

• Glucose Level

• Blood Pressure

• Skin Thickness

• Insulin Level

• BMI

• Diabetes Pedigree Function

• Age
""")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
---

## 📌 Project Details

**Project:** Diabetes Risk Prediction Web Application

**Domain:** Machine Learning Classification

**Algorithms Compared**
- Logistic Regression
- Random Forest Classifier

**Selected Model:** Logistic Regression

**Model Accuracy:** 76.62%

**Frameworks Used**
- Scikit-Learn
- Pandas
- Streamlit
- Matplotlib
- Seaborn

---


""")