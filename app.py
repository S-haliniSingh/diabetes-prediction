import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF
import datetime

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Diabetes Risk Checker", 
    page_icon="🩺", 
    layout="centered"
)

# --- 2. PWA (Install App) Logic ---
# Ye script phone mein "Install App" ka button dikhata hai
install_script = """
<script>
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        const installBtn = document.createElement('button');
        installBtn.innerText = '📲 Install App';
        installBtn.style.position = 'fixed';
        installBtn.style.bottom = '20px';
        installBtn.style.right = '20px';
        installBtn.style.zIndex = '999';
        installBtn.style.padding = '12px 20px';
        installBtn.style.backgroundColor = '#00e676';
        installBtn.style.color = 'white';
        installBtn.style.border = 'none';
        installBtn.style.borderRadius = '30px';
        installBtn.style.fontWeight = 'bold';
        installBtn.style.cursor = 'pointer';
        installBtn.style.boxShadow = '0 4px 15px rgba(0,230,118,0.5)';
        installBtn.style.fontSize = '16px';
        
        installBtn.onclick = async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                deferredPrompt = null;
                installBtn.style.display = 'none';
            }
        };
        
        document.body.appendChild(installBtn);
    });
</script>
"""
st.components.v1.html(install_script, height=0)

# --- 3. Custom CSS for Premium Design ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    .header-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
    }
    .main-title {
        color: #00e676;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: 1px;
        text-shadow: 0px 4px 15px rgba(0, 230, 118, 0.3);
    }
    .subtitle {
        font-size: 18px;
        color: #b0bec5;
        font-weight: 400;
    }
    .css-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .section-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 20px;
        border-bottom: 2px solid #00e676;
        padding-bottom: 10px;
        display: inline-block;
    }
    .stNumberInput label {
        color: #cfd8dc !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px !important;
    }
    .stNumberInput > div > div > input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: 1px solid #4CAF50;
        padding: 12px;
        font-weight: 600;
        font-size: 16px;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #00e676;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00e676 0%, #00b0ff 100%);
        color: white;
        border-radius: 30px;
        padding: 18px 40px;
        font-size: 20px;
        font-weight: 800;
        border: none;
        width: 100%;
        box-shadow: 0 4px 20px rgba(0, 230, 118, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00b0ff 0%, #00e676 100%);
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 8px 25px rgba(0, 230, 118, 0.7);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. Load Model ---
@st.cache_resource
def load_model():
    model = joblib.load("model/diabetes_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    return model, scaler

model, scaler = load_model()

# --- 5. Sidebar Navigation ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Select a page:", ["🏠 Home (Prediction)", "📊 Feature Guide", "📖 How to Use"])

# ==========================================
# PAGE 1: HOME (PREDICTION)
# ==========================================
if page == "🏠 Home (Prediction)":
    
    st.markdown("""
    <div class="header-container">
        <div class="main-title">🩺 Diabetes Predictor</div>
        <div class="subtitle">AI-powered health assessment. Enter your details below to get instant insights.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Patient Details</div>', unsafe_allow_html=True)
    
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

    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

    empty_col1, btn_col, empty_col2 = st.columns([1, 2, 1])
    with btn_col:
        predict_button = st.button("Predict Diabetes Risk", use_container_width=True)

    if predict_button:
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        scaled_data = scaler.transform(input_data)
        
        # Get Prediction and Probability
        prediction = model.predict(scaled_data)
        probability = model.predict_proba(scaled_data)[0]
        
        # Probability of Diabetes (Class 1)
        risk_percentage = probability[1] * 100
        
        st.divider()
        st.subheader("📊 Prediction Result")
        
        # Show Result with Probability
        if prediction[0] == 1:
            st.error(f"⚠️ **High Risk Detected:** The model predicts a **{risk_percentage:.1f}%** probability of Diabetes. Please consult a healthcare professional immediately.")
        else:
            safe_percentage = probability[0] * 100
            st.success(f"✅ **Low Risk:** The model predicts a **{safe_percentage:.1f}%** probability of being Non-Diabetic. Keep up the healthy lifestyle!")

        st.write("")
        
        # --- PDF Generation Logic ---
        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 15)
                self.cell(0, 10, 'Diabetes Prediction Report', 0, 1, 'C')
                self.ln(10)

        # Create PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        # Report Details
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 10, f"Date: {date_str}", 0, 1)
        pdf.cell(0, 10, "--- Patient Details ---", 0, 1)
        
        pdf.cell(90, 10, f"Pregnancies: {pregnancies}", 0, 0)
        pdf.cell(90, 10, f"Insulin: {insulin}", 0, 1)
        pdf.cell(90, 10, f"Glucose: {glucose} mg/dL", 0, 0)
        pdf.cell(90, 10, f"BMI: {bmi}", 0, 1)
        pdf.cell(90, 10, f"Blood Pressure: {blood_pressure} mm Hg", 0, 0)
        pdf.cell(90, 10, f"Pedigree Function: {dpf}", 0, 1)
        pdf.cell(90, 10, f"Skin Thickness: {skin_thickness} mm", 0, 0)
        pdf.cell(90, 10, f"Age: {age} years", 0, 1)
        
        pdf.ln(10)
        pdf.cell(0, 10, "--- Prediction Result ---", 0, 1)
        
        result_text = f"High Risk ({risk_percentage:.1f}% probability)" if prediction[0] == 1 else f"Low Risk ({probability[0]*100:.1f}% probability)"
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, f"Outcome: {result_text}", 0, 1)
        
        pdf.set_font("Helvetica", 'I', 10)
        pdf.ln(10)
        pdf.multi_cell(0, 10, "Disclaimer: This report is generated by an AI model for educational purposes only. It is not a substitute for professional medical advice.")
        
        # Convert PDF to bytes (New fpdf2 method)
        pdf_output = bytes(pdf.output())
        
        # Download Button
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_output,
            file_name=f"Diabetes_Report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# ==========================================
# PAGE 2: FEATURE GUIDE
# ==========================================
elif page == "📊 Feature Guide":
    st.title("📊 Feature Analysis Guide")
    st.markdown('<div class="subtitle">Understand which health metrics matter the most and their risk thresholds.</div>', unsafe_allow_html=True)
    
    st.info("💡 **Note:** Diabetes is a complex condition. A single high value does not always mean you have diabetes. The model analyzes all these features together to make a prediction.")
    
    st.divider()
    
    st.markdown("### 🔝 Which features are most important?")
    st.write("Our Machine Learning model (Random Forest) calculates how much each feature contributes to the prediction:")
    
    features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
    st.bar_chart(feature_importance_df.set_index('Feature'), color="#00e676")
    
    st.divider()
    
    st.markdown("### ⚠️ Risk Thresholds (Medical Guidelines)")
    st.write("Here are the generally accepted medical limits. If your values are above these, the risk of diabetes increases:")
    
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
    st.warning("🚨 **Important:** If your values are in the 'High Risk' category, please consult a healthcare professional.")

# ==========================================
# PAGE 3: HOW TO USE
# ==========================================
elif page == "📖 How to Use":
    st.title("📖 How to Use This App")
    st.markdown('<div class="subtitle">A simple, step-by-step guide to get the most out of this app.</div>', unsafe_allow_html=True)
    
    st.divider()

    st.markdown("""
    <style>
        .guide-card { background-color: rgba(255, 255, 255, 0.05); border-left: 5px solid #00e676; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .guide-card h3 { color: #00e676; margin-top: 0; }
        .guide-card p { color: #cfd8dc; font-size: 16px; line-height: 1.6; }
        .guide-list li { color: #cfd8dc; margin-bottom: 8px; font-size: 15px; }
        .guide-list strong { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div class="guide-card">
        <h3>🔍 Step 2: Click Predict</h3>
        <p>Once all the details are filled, simply click the glowing <b>"Predict Diabetes Risk"</b> button at the bottom of the page.</p>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div class="guide-card" style="border-left: 5px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.1);">
        <h3 style="color: #ff4b4b;">⚠️ Important Disclaimer</h3>
        <p>This app is for <b>educational and informational purposes only</b>. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider regarding any medical condition.</p>
    </div>
    """, unsafe_allow_html=True)
