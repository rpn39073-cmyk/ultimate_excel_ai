import pandas as pd
import numpy as np

def get_summary_statistics(df, numeric_cols):
    """Returns dataframe describe()"""
    if not numeric_cols: return pd.DataFrame()
    return df[numeric_cols].describe()

def generate_insights(df, numeric_cols, date_cols):
    """Generates textual insights."""
    insights = []
    insights.append(f"Dataset Shape: {len(df)} rows, {len(df.columns)} columns.")
    
    missing = df.isnull().sum().sum()
    if missing > 0:
        insights.append(f"Data quality: {missing} missing values remaining.")
    else:
        insights.append("Data quality: Clean (no missing values).")

    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.8)]
        if to_drop:
            insights.append(f"High correlations: {', '.join(to_drop[:3])} are strongly correlated with other variables.")

    if 'Is_Anomaly' in df.columns:
        n_anomalies = df['Is_Anomaly'].sum()
        if n_anomalies > 0:
            insights.append(f"Anomaly Alert: {n_anomalies} anomalies detected ({n_anomalies/len(df):.1%}).")

    if date_cols and numeric_cols:
        target = numeric_cols[0]
        # sort by date to get trend
        sorted_df = df.sort_values(date_cols[0])
        first_val = sorted_df[target].iloc[0]
        last_val = sorted_df[target].iloc[-1]
        
        # Avoid division by zero
        if first_val != 0:
            change = (last_val - first_val) / abs(first_val)
            direction = "increased" if change > 0 else "decreased"
            insights.append(f"Trend: {target} {direction} by {abs(change):.1%} over the time period.")

    return insights
