# 📊 Ultimate Excel AI Analyst (Enterprise SaaS Edition) 🚀

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg)](https://www.docker.com/)

A production-ready **Predictive Analytics Platform** that automatically analyzes, visualizes, and predicts trends from your Excel/CSV data. It features a robust **FastAPI** backend, a stunning **Streamlit** frontend, and **Docker** containerization for seamless deployment.

---

## ✨ Features
- **Automated Visualizations**: Instantly generates heatmaps, line charts, and distributions.
- **Predictive Analytics**: Forecast trends and train AutoML models with a single click.
- **Anomaly Detection**: Spot outliers in your data automatically.
- **Data Chat (NLU)**: Ask questions about your data in plain English.
- **Professional Reports**: Download a comprehensive Excel report with pivots, charts, and insights.

## 🌟 Architecture

The project is structured into a modular SaaS architecture:

```text
ultimate_excel_ai/
├── api/             # REST API using FastAPI
├── logic/           # Core Business Logic (Pure Python)
├── ui/              # Frontend Dashboard using Streamlit
├── config.py        # Centralized Configuration
├── Dockerfile       # Containerization setup
└── docker-compose.yml # SaaS Deployment setup
```

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/rpn39073-cmyk/ultimate_excel_ai.git
cd ultimate_excel_ai

# Install dependencies
pip install -r requirements.txt
```

## ▶️ How to Run

### 1. Local Mode (Analyst Mode)
Runs the Streamlit app using local logic modules directly (No API server needed). Ideal for single-user analysis.

```bash
python -m streamlit run ui/main.py
```
*Note: This mode sets `APP_MODE='LOCAL'` implicitly.*

### 2. SaaS Mode (DevOps Mode)
Runs the full stack using Docker: **FastAPI Backend** + **Streamlit Frontend**. The Frontend communicates with the Backend via REST API.

```bash
docker-compose up --build
```

- **Frontend Dashboard**: `http://localhost:8501`
- **Backend API**: `http://localhost:8000/docs`

## ☁️ Cloud Deployment

### Backend (Render/Railway/Heroku)
- Push the repo to GitHub.
- Connect your cloud provider.
- Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Streamlit Cloud/Vercel)
- Deploy the repository to Streamlit Community Cloud.
- Set Environment Variable: `API_URL=https://your-backend-url.com/api/v1`
- Entrypoint: `ui/main.py`

## 📄 License
This project is licensed under the MIT License.
