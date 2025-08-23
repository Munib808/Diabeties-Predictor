import streamlit as st
import numpy as np
import joblib


# 📁 Load trained model (trained without scaler)
model = joblib.load("model_ab.pkl")

# 🌐 Page config
st.set_page_config(page_title="Diabetes Predictor", page_icon="💉", layout="centered")

# 🎬 Title and animation
st.title("💉 AI Diabetes Prediction App")
st.caption("Using machine learning to predict diabetes — with style ✨")


# 🧾 Input fields
with st.form("form"):
    st.subheader("🧍 Patient Information")
    age = st.slider("Age", 10, 100, 30)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    rgn = st.radio("Region", ["Urban", "Rural"], horizontal=True)
    wt = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
    bmi = st.number_input("BMI", 10.0, 60.0, 24.0)
    wst = st.number_input("Waist (inches)", 20.0, 80.0, 34.0)
    sys = st.slider("Systolic BP", 80, 200, 120)
    dia = st.slider("Diastolic BP", 50, 120, 80)
    his = st.radio("Family History of Diabetes", ["No", "Yes"], horizontal=True)
    a1c = st.number_input("Hemoglobin A1c (%) — average blood sugar over 3 months ", 3.0, 15.0, 5.5)
    bsr = st.number_input("Random Blood Sugar", 50, 500, 90)
    vision = st.radio("Vision Issues", ["No", "Yes"], horizontal=True)
    exr = st.slider("Exercise (minutes/day)", 0, 120, 30)
    dipsia = st.radio("Dipsia (Excessive Thirst)", ["No", "Yes"], horizontal=True)
    uria = st.radio("Uria (Sugar/Protein in Urine)", ["No", "Yes"], horizontal=True)
    neph = st.radio("Nephropathy (Kidney issues)", ["No", "Yes"], horizontal=True)
    hdl = st.number_input("HDL Cholesterol", 10, 100, 50)

    predict_button = st.form_submit_button("🔍 Predict")

# 🧠 Predict
if predict_button:
    record = [
        age,
        1 if gender == "Male" else 0,
        0 if rgn == "Urban" else 1,
        wt,
        bmi,
        wst,
        sys,
        dia,
        1 if his == "Yes" else 0,
        a1c,
        bsr,
        1 if vision == "Yes" else 0,
        exr,
        1 if dipsia == "Yes" else 0,
        1 if uria == "Yes" else 0,
        1 if neph == "Yes" else 0,
        hdl
    ]

    proba = model.predict_proba(np.array([record]))[0]
    result = model.predict(np.array([record]))[0]

    # Display result
    st.markdown("---")
    if result == 1:
        st.error(f"🔴 Prediction: The patient is **Diabetic**. Please consult a doctor.")
        st.write(f"🧪 Probability of being diabetic: **{proba[1] * 100:.2f}%**")
    else:
        st.success(f"🟢 Prediction: The patient is **Not Diabetic**. Keep staying healthy!")
        st.write(f"🧪 Probability of not being diabetic: **{proba[0] * 100:.2f}%**")

