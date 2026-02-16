import sys, os
# Add the project root to sys.path (3 levels up from ui/main.py: ui -> ultimate_excel_ai -> root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from ultimate_excel_ai.ui.dashboard import render_dashboard

st.set_page_config(page_title="Ultimate Excel AI", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stButton>button { width: 100%; }
    .css-1d391kg { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()
