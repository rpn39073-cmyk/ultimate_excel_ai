import sys, os
# Add the project root to sys.path (3 levels up from ui/main.py: ui -> ultimate_excel_ai -> root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from ultimate_excel_ai.ui.dashboard import render_dashboard

st.set_page_config(page_title="Ultimate Excel AI", page_icon="📊", layout="wide")

# Custom CSS
# Custom CSS
st.markdown("""
<style>
    /* Main App Background and Font */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cards (Custom Class for containers) */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #E9ECEF;
    }
    
    /* Adjust spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Plotly Chart Container */
    .js-plotly-plot .plotly .modebar {
        display: none !important; /* Hide Plotly controls for clean look */
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()
