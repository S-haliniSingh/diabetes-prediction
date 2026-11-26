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

# --- 4. Sidebar Navigation ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Select a page:", ["🏠 Home (Prediction)", "📊 Feature Guide", "📖 How to Use"])

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
# PAGE 2: FEATURE GUIDE (NEW PAGE)
# ==========================================
elif page == "📊 Feature Guide":
    st.title("📊 Feature Analysis Guide")
    st.markdown('<div class="subtitle">Understand which health metrics matter the most and their risk thresholds.</div>', unsafe_allow_html=True)
    
    st.info("💡 **Note:** Diabetes is a complex condition. A single high value does not always mean you have diabetes. The model analyzes all these features together to make a prediction.")
    
    st.divider()
    
    # 1. Model ki Feature Importance nikalna
    st.markdown("### 🔝 Which features are most important?")
    st.write("Our Machine Learning model (Random Forest) calculates how much each feature contributes to the prediction:")
    
    # Feature names
    features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    # Model se importance nikalna
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
    # Graph banayein
    st.bar_chart(feature_importance_df.set_index('Feature'), color="#00e676")
    
    st.divider()
    
    # 2. Medical Thresholds (Limits) using HTML Table
    st.markdown("### ⚠️ Risk Thresholds (Medical Guidelines)")
    st.write("Here are the generally accepted medical limits. If your values are above these, the risk of diabetes increases:")
    
    # HTML Custom Table
    html_table = """
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px; color: white; font-size: 16px;">
        <tr style="background-color: #1a1a2e; color: #00e676;">
            <th style="padding: 12px; border: 1px solid #00e676; text-align: left;">Feature</th>
            <th style="padding: 12px; border: 1px solid #00e676; text-align: left;">Normal Range</th>
            <th style="padding: 12px; border: 1px solid #00e676; text-align: left;">High Risk (Above)</th>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #555;">Glucose</td>
            <td style="padding: 12px; border: 1px solid #555;">&lt; 140 mg/dL</td>
            <td style="padding: 12px; border: 1px solid #555;">&gt; 140 mg/dL</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #555;">Blood Pressure</td>
            <td style="padding: 12px; border: 1px solid #555;">&lt; 120 mm Hg</td>
            <td style="padding: 12px; border: 1px solid #555;">&gt; 120 mm Hg</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #555;">BMI</td>
            <td style="padding: 12px; border: 1px solid #555;">18.5 - 24.9</td>
            <td style="padding: 12px; border: 1px solid #555;">&gt; 24.9</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #555;">Insulin</td>
            <td style="padding: 12px; border: 1px solid #555;">&lt; 140 mu U/ml</td>
            <td style="padding: 12px; border: 1px solid #555;">&gt; 140 mu U/ml</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #555;">Skin Thickness</td>
            <td style="padding: 12px; border: 1px solid #555;">&lt; 25 mm</td>
            <td style="padding: 12px; border: 1px solid #555;">&gt; 25 mm</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #555;">Age</td>
            <td style="padding: 12px; border: 1px solid #555;">&lt; 45 years</td>
            <td style="padding: 12px; border: 1px solid #555;">&gt; 45 years</td>
        </tr>
    </table>
    """
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    st.warning("🚨 **Important:** If your values are in the 'High Risk' category, please consult a healthcare professional. Do not rely solely on this app for medical diagnosis.")
# ==========================================
# PAGE 3: HOW TO USE (GUIDE)
# ==========================================
elif page == "📖 How to Use":
    st.title("📖 How to Use This App")
    st.markdown('<div class="subtitle">A simple, step-by-step guide to get the most out of this app.</div>', unsafe_allow_html=True)
    
    st.divider()

    # Custom CSS specifically for this page's cards
    st.markdown("""
    <style>
        .guide-card {
            background-color: rgba(255, 255, 255, 0.05);
            border-left: 5px solid #00e676;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .guide-card h3 {
            color: #00e676;
            margin-top: 0;
        }
        .guide-card p {
            color: #cfd8dc;
            font-size: 16px;
            line-height: 1.6;
        }
        .guide-list li {
            color: #cfd8dc;
            margin-bottom: 8px;
            font-size: 15px;
        }
        .guide-list strong {
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

    # Step 1 Card
    st.markdown("""
    <div class="guide-card">
        <h3>👋 Step 1: Enter Your Details</h3>
        <p>Go to the <b>🏠 Home (Prediction)</b> page and fill in the input boxes. Here is what each medical term means:</p>
        <ul class="guide-list">
            <li><strong>Pregnancies:</strong> Number of times you have been pregnant.</li>
            <li><strong>Glucose Level:</strong> Your blood sugar level (in mg/dL).</li>
            <li><strong>Blood Pressure:</strong> Your blood pressure reading (in mm Hg).</li>
            <li><strong>Skin Thickness:</strong> Thickness of the skin fold on your triceps (in mm).</li>
            <li><strong>Insulin:</strong> Your insulin level (in mu U/ml).</li>
            <li><strong>BMI:</strong> Body Mass Index (a measure of body fat based on height and weight).</li>
            <li><strong>Diabetes Pedigree Function:</strong> A score that predicts diabetes risk based on family history.</li>
            <li><strong>Age:</strong> Your age in years.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Step 2 Card
    st.markdown("""
    <div class="guide-card">
        <h3>🔍 Step 2: Click Predict</h3>
        <p>Once all the details are filled, simply click the glowing <b>"🔍 Predict Diabetes Risk"</b> button at the bottom of the page.</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 3 Card
    st.markdown("""
    <div class="guide-card">
        <h3>📊 Step 3: Read the Result</h3>
        <p>After clicking predict, you will get one of two results:</p>
        <ul class="guide-list">
            <li><strong>✅ Low Risk (Green):</strong> Based on the data, the model thinks you are currently at low risk for diabetes.</li>
            <li><strong>⚠️ High Risk (Red):</strong> The model detects patterns similar to diabetic patients. You should consult a doctor for proper medical advice.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer Card (Red border for warning)
    st.markdown("""
    <div class="guide-card" style="border-left: 5px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.1);">
        <h3 style="color: #ff4b4b;">⚠️ Important Disclaimer</h3>
        <p>This app is for <b>educational and informational purposes only</b>. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider regarding any medical condition.</p>
    </div>
    """, unsafe_allow_html=True)
