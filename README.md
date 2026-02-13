# Ultimate Excel AI Analyst (Enterprise SaaS Edition) 🚀

A production-ready **Predictive Analytics Platform** featuring a **FastAPI** backend, **Streamlit** frontend, and **Docker** containerization.

## 🌟 Architecture

The project is refactored into a modular SaaS architecture:

-   **`ultimate_excel_ai/logic/`**: Core Business Logic (Pure Python).
-   **`ultimate_excel_ai/api/`**: REST API using **FastAPI**.
-   **`ultimate_excel_ai/ui/`**: Frontend Dashboard using **Streamlit**.
-   **`ultimate_excel_ai/config.py`**: Centralized Configuration.

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

### 1. Local Mode (Analyst Mode)
Runs the Streamlit app using local logic modules directly (No API server needed). Ideal for single-user analysis.

```bash
python -m streamlit run ultimate_excel_ai/main.py
```
*Note: This mode sets `APP_MODE='LOCAL'` implicitly.*

### 2. SaaS Mode (DevOps Mode)
Runs the full stack: **FastAPI Backend** + **Streamlit Frontend**. The Frontend communicates with the Backend via REST API.

```bash
docker-compose up --build
```
*Note: This mode sets `APP_MODE='SAAS'` via `API_URL` environment variable.*

-   **Frontend Dashboard**: `http://localhost:8501`
-   **Backend API**: `http://localhost:8000/docs`

## ☁️ Cloud Deployment

### Backend (Render/Railway)
-   Push the repo to GitHub.
-   Connect to Render/Railway.
-   Start Command: `uvicorn ultimate_excel_ai.api.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel/Streamlit Cloud)
-   Deploy the repository.
-   Set Environment Variable: `API_URL=https://your-backend-url.com/api/v1`
-   Command: `streamlit run ultimate_excel_ai/main.py`
