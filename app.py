import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Diabetes Risk Checker", 
    page_icon="🩺", 
    layout="centered"
)

# --- 2. Custom CSS for Modern Design ---
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: white;
    }
    
    /* Title styling */
    h1 {
        color: #4CAF50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #b0b0b0;
        margin-bottom: 30px;
    }
    
    /* Input box styling */
    .stNumberInput > div > div > input {
        background-color: #ffffff;
        color: #333333;
        border-radius: 10px;
        border: 1px solid #4CAF50;
        padding: 10px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #45a049 0%, #4CAF50 100%);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Load Model ---
@st.cache_resource
def load_model():
    model = joblib.load("model/diabetes_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    return model, scaler

model, scaler = load_model()

# --- 4. Title and Description ---
st.title("🩺 Diabetes Prediction App")
st.markdown('<div class="subtitle">Enter your medical details below to assess your risk of diabetes.</div>', unsafe_allow_html=True)

# --- 5. Input Fields in Columns ---
st.markdown("### 📝 Basic Details")
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
    glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=100)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)

with col2:
    insulin = st.number_input("Insulin (mu U/ml)", min_value=0, max_value=900, value=80)
    bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, format="%.1f")
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5, format="%.3f")
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)

st.divider()

# --- 6. Predict Button ---
empty_col1, btn_col, empty_col2 = st.columns([1, 2, 1])
with btn_col:
    predict_button = st.button("🔍 Predict Diabetes Risk", use_container_width=True)

# --- 7. Prediction Logic ---
if predict_button:
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)
    
    st.divider()
    st.subheader("📊 Prediction Result:")
    
    if prediction[0] == 1:
        st.error("⚠️ **High Risk:** The model predicts a high probability of Diabetes. Please consult a doctor immediately.")
    else:
        st.success("✅ **Low Risk:** The model predicts no Diabetes risk based on these details. Stay healthy!")
