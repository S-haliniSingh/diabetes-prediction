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
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
    }
    
    /* Title */
    h1 {
        color: #00e676;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #1a1a2e;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #cfd8dc;
        margin-bottom: 30px;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 5px !important;
    }

    /* Input Fields */
    .stNumberInput > div > div > input {
        background-color: #ffffff;
        color: #333333;
        border-radius: 10px;
        border: 2px solid #00e676;
        padding: 10px;
        font-weight: bold;
    }

    /* Predict Button */
    .stButton>button {
        background: linear-gradient(90deg, #00e676 0%, #00b0ff 100%);
        color: white;
        border-radius: 30px;
        padding: 15px 40px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #00b0ff 0%, #00e676 100%);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.6);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
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

# --- 4. Sidebar Navigation (Yahan se Page Change hoga) ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Select a page:", ["🏠 Home (Prediction)", "📖 How to Use"])

# ==========================================
# PAGE 1: HOME (PREDICTION)
# ==========================================
if page == "🏠 Home (Prediction)":
    st.title("🩺 Diabetes Prediction App")
    st.markdown('<div class="subtitle">Enter your medical details below to assess your risk of diabetes.</div>', unsafe_allow_html=True)

    st.markdown("### 📝 Patient Details")
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

    empty_col1, btn_col, empty_col2 = st.columns([1, 2, 1])
    with btn_col:
        predict_button = st.button("🔍 Predict Diabetes Risk", use_container_width=True)

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

# ==========================================
# PAGE 2: HOW TO USE (GUIDE)
# ==========================================
elif page == "📖 How to Use":
    st.title("📖 How to Use This App")
    st.markdown('<div class="subtitle">A simple guide for new users to understand how the prediction works.</div>', unsafe_allow_html=True)
    
    st.divider()

    st.markdown("""
    ### 👋 Welcome!
    This app uses a Machine Learning model to predict whether a person is at risk of Diabetes based on their medical details. Follow these steps to use the app:

    #### 📝 Step 1: Enter Your Details
    Go to the **Home (Prediction)** page and fill in the input boxes. Here is what each term means:
    
    *   **Pregnancies:** How many times you have been pregnant.
    *   **Glucose Level:** Your blood sugar level (in mg/dL).
    *   **Blood Pressure:** Your blood pressure reading (in mm Hg).
    *   **Skin Thickness:** Thickness of the skin fold on your triceps (in mm).
    *   **Insulin:** Your insulin level (in mu U/ml).
    *   **BMI:** Body Mass Index (a measure of body fat based on height and weight).
    *   **Diabetes Pedigree Function:** A score that predicts diabetes risk based on family history.
    *   **Age:** Your age in years.

    #### 🔍 Step 2: Click Predict
    Once all the details are filled, click the **"Predict Diabetes Risk"** button.

    #### 📊 Step 3: Read the Result
    *   **✅ Low Risk (Green):** Based on the data, the model thinks you are currently at low risk.
    *   **⚠️ High Risk (Red):** The model detects patterns similar to diabetic patients. You should consult a doctor for proper medical advice.

    ---
    ### ⚠️ Disclaimer
    **This app is for educational and informational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider regarding any medical condition.
    """)
