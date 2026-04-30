import sys, os
# Add the project root to sys.path (3 levels up from ui/main.py: ui -> ultimate_excel_ai -> root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from ultimate_excel_ai.ui.dashboard import render_dashboard

st.set_page_config(page_title="Ultimate Excel AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Initialize default theme if not present (Blinkit defaults)
if 'theme_primary' not in st.session_state:
    st.session_state['theme_primary'] = "#FAD02C" # Blinkit Yellow
if 'theme_bg' not in st.session_state:
    st.session_state['theme_bg'] = "#F0F2F5" # Light Gray BG
if 'theme_card_bg' not in st.session_state:
    st.session_state['theme_card_bg'] = "#FFFFFF" # White cards
if 'theme_text' not in st.session_state:
    st.session_state['theme_text'] = "#333333"

# Custom Dynamic CSS
st.markdown(f"""
<style>
    /* Main App Background and Font */
    .stApp {{
        background-color: {st.session_state['theme_bg']};
        color: {st.session_state['theme_text']};
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {st.session_state['theme_primary']} !important;
        border-right: none;
    }}
    
    section[data-testid="stSidebar"] * {{
        color: #333333 !important; /* Sidebar text always dark for yellow */
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, p, span {{
        color: {st.session_state['theme_text']} !important;
    }}
    
    /* Buttons */
    .stButton>button {{
        width: 100%;
        background-color: {st.session_state['theme_primary']};
        color: #333 !important;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    .stButton>button:hover {{
        filter: brightness(0.95);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    /* Cards (Custom Class for containers) */
    .metric-card {{
        background-color: {st.session_state['theme_card_bg']};
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: left;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }}
    
    .metric-card h3 {{
        font-size: 0.9rem;
        color: {st.session_state['theme_text']} !important;
        opacity: 0.8;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
        font-weight: 600;
    }}
    
    .metric-card h2 {{
        font-size: 1.8rem;
        color: {st.session_state['theme_text']} !important;
        margin: 0;
        font-weight: 800;
    }}
    
    /* Adjust spacing for Dense Power BI Look */
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }}
    
    div[data-testid="column"] {{
        padding: 0 0.5rem; /* Reduce gap between columns */
    }}
    
    /* Plotly Chart Container */
    .js-plotly-plot .plotly .modebar {{
        display: none !important;
    }}

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        background-color: transparent;
        padding: 5px 15px;
        color: {st.session_state['theme_text']};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        color: #333333 !important;
        background-color: {st.session_state['theme_primary']} !important;
        border-radius: 4px;
        border-bottom: none !important;
    }}

    /* Hide Top Padding/Header */
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()
