from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class InsightResponse(BaseModel):
    insights: List[str]

class PredictionRequest(BaseModel):
    filename: str
    target_column: str

class PredictionResponse(BaseModel):
    model_type: str
    metrics: Dict[str, float]

class ForecastRequest(BaseModel):
    filename: str
    date_column: str
    target_column: str
    periods: int = 30

class ForecastResponse(BaseModel):
    forecast: List[Dict[str, Any]]

class AnomalyResponse(BaseModel):
    anomaly_count: int
    anomalies: List[Dict[str, Any]]
