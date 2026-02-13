import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, IsolationForest
from sklearn.metrics import r2_score, accuracy_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder

class MachineLearningEngine:
    def __init__(self):
        self.predictor_model = None
        self.forecaster_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.le = LabelEncoder()

    def train_predictor(self, df, target_col):
        """AutoML for Regression (Numeric) or Classification (Categorical)."""
        df = df.dropna(subset=[target_col])
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Feature Engineering: Dates
        for col in X.select_dtypes(include=['datetime']).columns:
            X[col + '_year'] = X[col].dt.year
            X[col + '_month'] = X[col].dt.month
            X[col + '_day'] = X[col].dt.day
            X = X.drop(columns=[col])
            
        # Feature Engineering: Categorical
        cat_cols = X.select_dtypes(include=['object', 'category']).columns
        if not cat_cols.empty:
            X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
            
        # Target Type Detection
        is_classification = False
        if pd.api.types.is_numeric_dtype(y):
            if y.nunique() < 10 and y.dtype == 'int64':
                 is_classification = True
        else:
            is_classification = True
            
        if is_classification:
            y = self.le.fit_transform(y.astype(str))
            
        # Split & Train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        metrics = {}
        if is_classification:
            self.predictor_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.predictor_model.fit(X_train, y_train)
            preds = self.predictor_model.predict(X_test)
            metrics['accuracy'] = accuracy_score(y_test, preds)
            metrics['type'] = 'Classification'
        else:
            self.predictor_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.predictor_model.fit(X_train, y_train)
            preds = self.predictor_model.predict(X_test)
            metrics['r2_score'] = r2_score(y_test, preds)
            metrics['mae'] = mean_absolute_error(y_test, preds)
            metrics['type'] = 'Regression'
            
        return self.predictor_model, metrics

    def forecast_series(self, df, date_col, value_col, periods=30, freq='D'):
        """Time Series Forecasting using Lag-based Random Forest."""
        df_agg = df.groupby(date_col)[value_col].sum().reset_index()
        df_agg = df_agg.sort_values(date_col)
        df_agg.set_index(date_col, inplace=True)
        
        for i in range(1, 4):
            df_agg[f'lag_{i}'] = df_agg[value_col].shift(i)
        df_agg.dropna(inplace=True)
        
        if df_agg.empty: return None
            
        X = df_agg[[c for c in df_agg.columns if 'lag' in c]]
        y = df_agg[value_col]
        
        self.forecaster_model.fit(X, y)
        
        future_dates = pd.date_range(start=df_agg.index[-1], periods=periods + 1, freq=freq)[1:]
        forecasts = []
        current_lags = list(df_agg.iloc[-1][[f'lag_{i}' for i in range(1, 4)]].values)
        last_val = df_agg.iloc[-1][value_col]
        current_lags = [last_val] + current_lags[:-1]
        
        for _ in range(periods):
            pred = self.forecaster_model.predict([current_lags])[0]
            forecasts.append(pred)
            current_lags = [pred] + current_lags[:-1]
            
        return pd.DataFrame({'Date': future_dates, 'Forecast': forecasts})

    def detect_anomalies(self, df, numeric_cols, contamination=0.05):
        """Anomaly Detection via Isolation Forest."""
        if not numeric_cols: return df
        iso = IsolationForest(contamination=contamination, random_state=42)
        X = df[numeric_cols].fillna(0)
        preds = iso.fit_predict(X)
        df['Is_Anomaly'] = preds == -1
        return df
