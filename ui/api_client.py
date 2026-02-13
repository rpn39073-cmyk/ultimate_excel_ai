import requests
import pandas as pd
import io
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def upload_file(self, file_obj, filename):
        files = {'file': (filename, file_obj, 'application/octet-stream')}
        try:
            response = requests.post(f"{self.base_url}/upload", files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def analyze(self, filename):
        try:
            response = requests.post(f"{self.base_url}/analyze", params={"filename": filename})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def predict(self, filename, target_col):
        payload = {"filename": filename, "target_column": target_col}
        try:
            response = requests.post(f"{self.base_url}/predict", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def forecast(self, filename, date_col, target_col, periods):
        payload = {
            "filename": filename,
            "date_column": date_col,
            "target_column": target_col,
            "periods": periods
        }
        try:
            response = requests.post(f"{self.base_url}/forecast", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def detect_anomalies(self, filename):
        try:
            response = requests.post(f"{self.base_url}/anomalies", params={"filename": filename})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
