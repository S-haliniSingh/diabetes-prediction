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

# --- 2. Session State for Theme ---
# Agar pehli baar app khul rahi hai, to default theme Dark rakhein
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# --- 3. Sidebar Navigation & Theme Toggle ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00BFFF;'>🩺 Diabetes AI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Theme Toggle Button
    theme_choice = st.toggle("🌙 Dark Mode", value=(st.session_state.theme == 'Dark'))
    st.session_state.theme = 'Dark' if theme_choice else 'Light'
    
    st.markdown("---")
    
    # Navigation Menu
    page = st.radio("Navigation Menu", ["🏠 Prediction", "📊 Feature Guide", "📖 How to Use"])
    st.markdown("---")
    st.info("This app uses Machine Learning to assess Diabetes risk based on medical inputs.")

# --- 4. Custom CSS based on Theme Selection ---
if st.session_state.theme == 'Dark':
    # DARK THEME (Black & Sky Blue)
    bg_color = "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)"
    text_color = "#ffffff"
    subtext_color = "#b0bec5"
    card_bg = "rgba(255, 255, 255, 0.05)"
    card_border = "rgba(255, 255, 255, 0.1)"
    input_bg = "rgba(0, 0, 0, 0.2)"
    input_text = "#ffffff"
    primary_color = "#00BFFF" # Sky Blue
    sidebar_bg = "#1a1a2e"
else:
    # LIGHT THEME (White & Black)
    bg_color = "#f4f7f6"
    text_color = "#1a1a2e"
    subtext_color = "#555555"
    card_bg = "#ffffff"
    card_border = "#e0e0e0"
    input_bg = "#f9f9f9"
    input_text = "#333333"
    primary_color = "#007BFF" # Standard Blue for Light mode
    sidebar_bg = "#ffffff"

st.markdown(f"""
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border};
    }}
    
    .hero-section {{
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
    }}
    
    .hero-title {{
        color: {primary_color};
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 10px;
        letter-spacing: 1px;
        text-shadow: 0px 4px 20px {primary_color}66; 
    }}
    
    .hero-subtitle {{
        font-size: 18px;
        color: {subtext_color};
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }}

    .glass-card {{
        background: {card_bg};
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(12px);
        border: 1px solid {card_border};
        margin-bottom: 25px;
    }}
    
    .section-title {{
        color: {text_color};
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 25px;
    }}

    .stNumberInput label {{
        color: {subtext_color} !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        margin-bottom: 8px !important;
    }}

    .stNumberInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border-radius: 10px;
        border: 1px solid {card_border};
        padding: 14px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }}
    
    .stNumberInput > div > div > input:focus {{
        border-color: {primary_color};
        box-shadow: 0 0 0 2px {primary_color}44;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {primary_color} 0%, #007BFF 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 16px 40px;
        font-size: 18px;
        font-weight: 700;
        border: none;
        width: 100%;
        box-shadow: 0 4px 15px {primary_color}55;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px {primary_color}88;
    }}
    
    .guide-card {{ 
        background-color: {card_bg}; 
        border-left: 4px solid {primary_color}; 
        border-radius: 12px; 
        padding: 25px; 
        margin-bottom: 20px; 
    }}
    .guide-card h3 {{ color: {primary_color}; }}
    .guide-card p, .guide-list li {{ color: {text_color}; }}
    
</style>
""", unsafe_allow_html=True)

# --- 5. Load Model ---
@st.cache_resource
def load_model():
    model = joblib.load("model/diabetes_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    return model, scaler

model, scaler = load_model()

# ==========================================
# PAGE 1: HOME (PREDICTION)
# ==========================================
if page == "🏠 Prediction":
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">Diabetes Predictor</div>
        <div class="hero-subtitle">AI-powered health assessment. Enter your medical details below to get instant, data-driven insights.</div>
    </div>
    """, unsafe_allow_html=True)

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
        
        # --- PDF Generation ---
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
        pdf.multi_cell(0, 10, "Disclaimer: This report is generated by an AI model for educational purposes only.")
        
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
    st.markdown(f'<div class="subtitle" style="color:{subtext_color};">Understand which health metrics matter the most.</div>', unsafe_allow_html=True)
    
    st.divider()
    
    features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
  
       # --- CHART FIX (Horizontal Bar) ---
    # Colors define karein (Sky Blue to Dark Blue)
    if st.session_state.theme == 'Dark':
        chart_colors = ['#00BFFF', '#0099CC', '#007399', '#005C7A', '#004D66', '#003D52', '#002E3D', '#001F29']
        font_color = "white"
    else:
        chart_colors = ['#007BFF', '#0062CC', '#004999', '#002F66', '#001533', '#000000', '#000000', '#000000']
        font_color = "black"

    fig = px.bar(
        feature_importance_df, 
        x='Importance', 
        y='Feature', 
        orientation='h', # Horizontal bar ke liye
        color='Feature',
        color_discrete_sequence=chart_colors,
        text_auto='.3f' # Bars ke upar value dikhane ke liye
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=font_color,
        xaxis_title="Importance Score",
        yaxis_title="",
        showlegend=False, # Legend ki zaroorat nahi hai
        margin=dict(l=0, r=0, t=10, b=0),
        height=400
    )
    
    # Bars ko aur sundar banane ke liye
    fig.update_traces(
        textposition='outside',
        marker_line_color='black',
        marker_line_width=0
    )
    
    # Y-axis ko reverse karein taaki sabse important feature sabse upar dikhe
    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig, use_container_width=True)
    # ---------------------------------- 
    st.divider()
    
    st.markdown("### ⚠️ Risk Thresholds (Medical Guidelines)")
    
    # Table Color based on theme
    th_color = '#00BFFF' if st.session_state.theme == 'Dark' else '#007BFF'
    td_border = '#555' if st.session_state.theme == 'Dark' else '#ccc'
    
    html_table = f"""
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px; color: {text_color}; font-size: 16px;">
        <tr style="background-color: {card_bg}; color: {th_color};">
            <th style="padding: 12px; border: 1px solid {th_color}; text-align: left;">Feature</th>
            <th style="padding: 12px; border: 1px solid {th_color}; text-align: left;">Normal Range</th>
            <th style="padding: 12px; border: 1px solid {th_color}; text-align: left;">High Risk (Above)</th>
        </tr>
        <tr><td style="padding: 12px; border: 1px solid {td_border};">Glucose</td><td style="padding: 12px; border: 1px solid {td_border};">&lt; 140</td><td style="padding: 12px; border: 1px solid {td_border};">&gt; 140</td></tr>
        <tr><td style="padding: 12px; border: 1px solid {td_border};">Blood Pressure</td><td style="padding: 12px; border: 1px solid {td_border};">&lt; 120</td><td style="padding: 12px; border: 1px solid {td_border};">&gt; 120</td></tr>
        <tr><td style="padding: 12px; border: 1px solid {td_border};">BMI</td><td style="padding: 12px; border: 1px solid {td_border};">18.5 - 24.9</td><td style="padding: 12px; border: 1px solid {td_border};">&gt; 24.9</td></tr>
        <tr><td style="padding: 12px; border: 1px solid {td_border};">Insulin</td><td style="padding: 12px; border: 1px solid {td_border};">&lt; 140</td><td style="padding: 12px; border: 1px solid {td_border};">&gt; 140</td></tr>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

# ==========================================
# PAGE 3: HOW TO USE
# ==========================================
elif page == "📖 How to Use":
    st.title("📖 How to Use This App")
    st.divider()

    st.markdown("""
    <div class="guide-card">
        <h3>👋 Step 1: Enter Your Details</h3>
        <p>Go to the <b>🏠 Prediction</b> page and fill in the input boxes.</p>
    </div>
    <div class="guide-card">
        <h3>🔍 Step 2: Analyze Risk</h3>
        <p>Once all the details are filled, simply click the glowing <b>"Analyze Risk"</b> button.</p>
    </div>
    <div class="guide-card" style="border-left: 4px solid #ff4b4b;">
        <h3 style="color: #ff4b4b;">⚠️ Important Disclaimer</h3>
        <p>This app is for <b>educational purposes only</b>. Consult a doctor for medical advice.</p>
    </div>
    """, unsafe_allow_html=True)
