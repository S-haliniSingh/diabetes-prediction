import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF
import datetime
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Diabetes Risk Checker", 
    page_icon="🩺", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. Custom CSS for Premium UI ---
st.markdown("""
<style>
    /* Hide Streamlit default header, footer and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: beige;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
    }
    
    .hero-title {
        color: #00e676;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 10px;
        letter-spacing: 1px;
        text-shadow: 0px 4px 20px rgba(0, 230, 118, 0.4);
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: #b0bec5;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 25px;
    }
    
    /* Section Title */
    .section-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Input Labels */
    .stNumberInput label {
        color: #cfd8dc !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 8px !important;
    }

    /* Input Fields */
    .stNumberInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.2) !important;
        color: #ffffff !important;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #87CEEB;
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.2);
        background-color: rgba(0, 0, 0, 0.4) !important;
    }

    /* Primary Button (Gradient) */
    .stButton>button {
        background: linear-gradient(135deg, #00e676 0%, #00b0ff 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 16px 40px;
        font-size: 18px;
        font-weight: 700;
        border: none;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #00b0ff 0%, #00e676 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.5);
        color: #ffffff;
    }
    
    /* Success/Error boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid;
        background-color: rgba(0,0,0,0.2);
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
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00e676;'>🩺 Diabetes AI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation Menu", ["🏠 Prediction", "📊 Feature Guide", "📖 How to Use"])
    st.markdown("---")
    st.info("This app uses Machine Learning to assess Diabetes risk based on medical inputs.")

# ==========================================
# PAGE 1: HOME (PREDICTION)
# ==========================================
if page == "🏠 Prediction":
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Diabetes Predictor</div>
        <div class="hero-subtitle">AI-powered health assessment. Enter your medical details below to get instant, data-driven insights.</div>
    </div>
    """, unsafe_allow_html=True)

    # Input Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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

    # Predict Button
    empty_col1, btn_col, empty_col2 = st.columns([1, 2, 1])
    with btn_col:
        predict_button = st.button("Analyze Risk", use_container_width=True)

    if predict_button:
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        scaled_data = scaler.transform(input_data)
        
        prediction = model.predict(scaled_data)
        probability = model.predict_proba(scaled_data)[0]
        risk_percentage = probability[1] * 100
        
        st.divider()
        st.subheader("📊 Prediction Result")
        
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

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
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
        
        pdf_output = bytes(pdf.output())
        
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
    
    st.markdown("### 🔝 Feature Importance")
    st.write("Our Machine Learning model calculates how much each feature contributes to the prediction:")
    
    features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
    # --- CHART FIX ---
    fig = px.bar(feature_importance_df, x='Feature', y='Importance', color_discrete_sequence=['#00e676'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Features",
        yaxis_title="Importance Score",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
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
        .guide-card { background-color: rgba(255, 255, 255, 0.03); border-left: 4px solid #00e676; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); backdrop-filter: blur(10px); }
        .guide-card h3 { color: #00e676; margin-top: 0; font-size: 20px; }
        .guide-card p { color: #cfd8dc; font-size: 16px; line-height: 1.6; }
        .guide-list li { color: #cfd8dc; margin-bottom: 10px; font-size: 15px; }
        .guide-list strong { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="guide-card">
        <h3>👋 Step 1: Enter Your Details</h3>
        <p>Go to the <b>🏠 Prediction</b> page and fill in the input boxes. Here is what each medical term means:</p>
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
        <h3>🔍 Step 2: Analyze Risk</h3>
        <p>Once all the details are filled, simply click the glowing <b>"Analyze Risk"</b> button at the bottom of the page.</p>
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
    <div class="guide-card" style="border-left: 4px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.05);">
        <h3 style="color: #ff4b4b;">⚠️ Important Disclaimer</h3>
        <p>This app is for <b>educational and informational purposes only</b>. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider regarding any medical condition.</p>
    </div>
    """, unsafe_allow_html=True)
