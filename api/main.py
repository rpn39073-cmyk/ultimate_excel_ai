from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import pandas as pd
from ultimate_excel_ai.config import settings
from ultimate_excel_ai.logic import data, ml, analysis, nlu
import logging
from ultimate_excel_ai.api import schemas

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo purposes (production would use DB/S3)
# We store dataframes in a global dict keyed by filename for simplicity in this session
# In real SaaS, use Redis or a Database with session IDs.
DATA_STORE = {}

@app.get("/")
def root():
    return {"message": "Ultimate Excel AI Analyst API is running"}

@app.post(f"{settings.API_V1_STR}/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        logger.info(f"Received file: {file.filename}, Size: {len(content)} bytes")
        
        # Save to Disk (Temp)
        file_location = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(content)
            
        df, msg = data.load_data(io.BytesIO(content), file.filename)
        
        if df is None:
            logger.error(f"Failed to load data: {msg}")
            raise HTTPException(status_code=400, detail=msg)
            
        # Clean Data
        df, num, cat, date, stats = data.process_data(df)
        
        # Store in memory (and potentially cache on disk via file_location)
        DATA_STORE[file.filename] = {
            "df": df,
            "num": num,
            "cat": cat,
            "date": date,
            "stats": stats
        }
        
        return {
            "filename": file.filename, 
            "status": "success", 
            "rows": len(df), 
            "columns": len(df.columns),
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_data(filename):
    if filename not in DATA_STORE:
        raise HTTPException(status_code=404, detail="File not found")
    return DATA_STORE[filename]

@app.post(f"{settings.API_V1_STR}/analyze", response_model=schemas.InsightResponse)
def analyze_data(filename: str):
    logger.info(f"Analyzing {filename}")
    d = get_data(filename)
    insights = analysis.generate_insights(d['df'], d['num'], d['date'])
    return {"insights": insights}

@app.post(f"{settings.API_V1_STR}/predict", response_model=schemas.PredictionResponse)
def predict(req: schemas.PredictionRequest):
    d = get_data(req.filename)
    if req.target_column not in d['df'].columns:
         raise HTTPException(status_code=400, detail="Target column not found")
         
    engine = ml.MachineLearningEngine()
    model, metrics = engine.train_predictor(d['df'], req.target_column)
    return {"model_type": metrics.get('type'), "metrics": metrics}

@app.post(f"{settings.API_V1_STR}/forecast", response_model=schemas.ForecastResponse)
def forecast(req: schemas.ForecastRequest):
    d = get_data(req.filename)
    engine = ml.MachineLearningEngine()
    forecast_df = engine.forecast_series(d['df'], req.date_column, req.target_column, req.periods)
    
    if forecast_df is None:
        raise HTTPException(status_code=400, detail="Could not generate forecast")
        
    return {"forecast": forecast_df.to_dict(orient="records")}

@app.post(f"{settings.API_V1_STR}/anomalies", response_model=schemas.AnomalyResponse)
def detect_anomalies(filename: str):
    d = get_data(filename)
    engine = ml.MachineLearningEngine()
    df_anom = engine.detect_anomalies(d['df'].copy(), d['num'])
    
    anoms = df_anom[df_anom['Is_Anomaly'] == True]
    return {
        "anomaly_count": len(anoms),
        "anomalies": anoms.head(100).to_dict(orient="records") # Limit return size
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ultimate_excel_ai.api.main:app", host="0.0.0.0", port=8000, reload=True)
