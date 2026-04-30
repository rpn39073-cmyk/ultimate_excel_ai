import sys, os
# Add the project root to sys.path (3 levels up from ui/main.py: ui -> ultimate_excel_ai -> root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from ultimate_excel_ai.ui.dashboard import render_dashboard

st.set_page_config(page_title="Ultimate Excel AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Initialize default theme if not present
if 'theme_primary' not in st.session_state:
    st.session_state['theme_primary'] = "#00D2FF" # Cyan/Blue glowing
if 'theme_bg' not in st.session_state:
    st.session_state['theme_bg'] = "#0E1117" # Dark BG
if 'theme_card_bg' not in st.session_state:
    st.session_state['theme_card_bg'] = "#1E2127" # Slightly lighter dark
if 'theme_text' not in st.session_state:
    st.session_state['theme_text'] = "#FAFAFA"

# Custom Dynamic CSS
st.markdown(f"""
<style>
    /* Main App Background and Font */
    .stApp {{
        background-color: {st.session_state['theme_bg']};
        color: {st.session_state['theme_text']};
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {st.session_state['theme_card_bg']} !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, p, span {{
        color: {st.session_state['theme_text']} !important;
    }}
    
    /* Buttons */
    .stButton>button {{
        width: 100%;
        background-color: {st.session_state['theme_primary']};
        color: #fff !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px {st.session_state['theme_primary']}40;
    }}
    .stButton>button:hover {{
        filter: brightness(1.1);
        box-shadow: 0 6px 15px {st.session_state['theme_primary']}60;
        color: #fff !important;
    }}
    
    /* Cards (Custom Class for containers) */
    .metric-card {{
        background-color: {st.session_state['theme_card_bg']};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        border: 1px solid {st.session_state['theme_primary']}50;
    }}
    
    .metric-card h3 {{
        font-size: 1rem;
        color: {st.session_state['theme_text']} !important;
        opacity: 0.7;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .metric-card h2 {{
        font-size: 2rem;
        color: {st.session_state['theme_primary']} !important;
        margin: 0;
        font-weight: 700;
        text-shadow: 0 0 10px {st.session_state['theme_primary']}30;
    }}
    
    /* Adjust spacing */
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}
    
    /* Plotly Chart Container */
    .js-plotly-plot .plotly .modebar {{
        display: none !important; /* Hide Plotly controls for clean look */
    }}

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: {st.session_state['theme_text']};
    }}
    .stTabs [aria-selected="true"] {{
        color: {st.session_state['theme_primary']} !important;
        border-bottom-color: {st.session_state['theme_primary']} !important;
    }}

    /* Hide Top Padding/Header */
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()
