import streamlit as st

def get_css(theme: str) -> str:
    """
    Returns the complete CSS string based on the selected theme.
    """
    if theme == "Dark":
        bg_gradient = "linear-gradient(135deg, #0B1220 0%, #111B2E 100%)"
        glass_bg = "rgba(255, 255, 255, 0.06)"
        glass_border = "1px solid rgba(255, 255, 255, 0.12)"
        text_main = "#E6EDF7"
        text_muted = "#9AA8BF"
        shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.3)"
    else:
        bg_gradient = "linear-gradient(135deg, #F4F7FB 0%, #E8EEF7 100%)"
        glass_bg = "rgba(255, 255, 255, 0.65)"
        glass_border = "1px solid rgba(0, 0, 0, 0.08)"
        text_main = "#0F1B2D"
        text_muted = "#5B6B82"
        shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.05)"

    css = f"""
    <style>
        /* --- CSS VARIABLES --- */
        :root {{
            --primary: #2F80ED;
            --secondary: #14B8A6;
            --risk-low: #22C55E;
            --risk-mod: #F59E0B;
            --risk-high: #EF4444;
            
            --bg-gradient: {bg_gradient};
            --glass-bg: {glass_bg};
            --glass-border: {glass_border};
            --glass-shadow: {shadow};
            
            --text-main: {text_main};
            --text-muted: {text_muted};
            
            --radius-lg: 20px;
            --radius-md: 12px;
            --radius-sm: 8px;
            
            --font-main: -apple-system, "SF Pro Display", "Inter", "Segoe UI", sans-serif;
        }}

        /* --- GLOBAL STYLES --- */
        .stApp {{
            background: var(--bg-gradient);
            color: var(--text-main);
            font-family: var(--font-main);
            -webkit-font-smoothing: antialiased;
        }}
        
        /* Hide default Streamlit elements */
        #MainMenu, footer, header, [data-testid="collapsedControl"] {{visibility: hidden;}}
        
        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{
            color: var(--text-main);
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        p, span, label {{
            color: var(--text-main);
            line-height: 1.5;
        }}
        .muted-text {{
            color: var(--text-muted) !important;
            font-size: 0.9rem;
        }}

        /* --- GLASSMORPHISM CARDS --- */
        .glass-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            border: var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 24px;
            box-shadow: var(--glass-shadow);
            margin-bottom: 24px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeInUp 0.6s ease-out forwards;
        }}
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.15);
        }}

        /* --- NAVIGATION CARDS --- */
        .nav-card {{
            cursor: pointer;
            text-align: center;
            padding: 20px;
            border: 2px solid transparent;
        }}
        .nav-card.active {{
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(47, 128, 237, 0.3);
        }}

        /* --- INPUTS & WIDGETS --- */
        .stNumberInput > div > div > input {{
            background-color: transparent !important;
            color: var(--text-main) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-sm) !important;
            padding: 10px 14px !important;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        .stNumberInput > div > div > input:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(47, 128, 237, 0.2) !important;
        }}
        .stNumberInput label {{
            color: var(--text-muted) !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }}

        /* --- BUTTONS --- */
        .stButton > button {{
            background: var(--primary);
            color: #FFFFFF;
            border: none;
            border-radius: var(--radius-md);
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.2s ease;
            width: 100%;
        }}
        .stButton > button:hover {{
            background: #1C6DD0;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(47, 128, 237, 0.4);
        }}
        
        /* --- BADGES --- */
        .badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .badge-low {{ background: rgba(34, 197, 94, 0.15); color: var(--risk-low); border: 1px solid var(--risk-low); }}
        .badge-mod {{ background: rgba(245, 158, 11, 0.15); color: var(--risk-mod); border: 1px solid var(--risk-mod); }}
        .badge-high {{ background: rgba(239, 68, 68, 0.15); color: var(--risk-high); border: 1px solid var(--risk-high); }}

        /* --- ANIMATIONS --- */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @media (prefers-reduced-motion: reduce) {{
            .glass-card, .stButton > button {{ animation: none; transition: none; }}
        }}

        /* --- MOBILE RESPONSIVENESS --- */
        @media (max-width: 768px) {{
            .glass-card {{ padding: 16px; }}
            .nav-card {{ margin-bottom: 12px; }}
        }}
    </style>
    """
    return css
