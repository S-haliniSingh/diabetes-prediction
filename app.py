import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- 1. Page Configuration (Tab ka naam aur Icon) ---
st.set_page_config(
    page_title="Diabetes Risk Checker", 
    page_icon="🩺", 
    layout="centered"
)

# --- 2. Model aur Scaler Load karein ---
@st.cache_resource
def load_model():
    # GitHub ke liye path change kiya gaya hai
    model = joblib.load("model/diabetes_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    return model, scaler

model, scaler = load_model()

# --- 3. Title aur Description ---
st.title("Diabetes Prediction App 🩺")
st.markdown("""
Welcome to the **Diabetes Risk Checker**.  
Yahan apni medical details bharein aur check karein ki aapko diabetes ka khatra hai ya nahi. 
Saari values sahi se bharein taaki prediction accurate ho.
""")
st.divider()

# --- 4. Input Fields ko 2 Columns mein baantna ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Details")
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
    glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=100)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)

with col2:
    st.subheader("Medical Details")
    insulin = st.number_input("Insulin (mu U/ml)", min_value=0, max_value=900, value=80)
    bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, format="%.1f")
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5, format="%.3f")
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)

st.divider()

# --- 5. Predict Button aur Result ---
# Center mein button laane ke liye ek khaali column use kar rahe hain
empty_col1, btn_col, empty_col2 = st.columns([1, 2, 1])

with btn_col:
    predict_button = st.button("🔍 Predict Diabetes Risk", use_container_width=True)

if predict_button:
    # Data ko array mein convert karein
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    
    # Scaling apply karein
    scaled_data = scaler.transform(input_data)
    
    # Prediction karein
    prediction = model.predict(scaled_data)
    
    st.subheader("Prediction Result:")
    
    if prediction[0] == 1:
        st.error("⚠️ **High Risk:** Aapko Diabetes ho sakta hai. Kripya jald doctor se salah lein.")
    else:
        st.success("✅ **Low Risk:** Aapko Diabetes ka koi khatra nahi hai. Aap fit hain!")
