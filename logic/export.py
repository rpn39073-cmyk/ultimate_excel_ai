import pandas as pd
import io

def generate_excel_report(df, pivots, forecast_df=None, anomaly_df=None, model_metrics=None, insights=None):
    """Generates multi-sheet Excel report."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        
        if insights or model_metrics:
            summary_data = []
            if model_metrics:
                summary_data.append(["Model Metrics", ""])
                for k, v in model_metrics.items(): summary_data.append([k, v])
            if insights:
                summary_data.append(["Insights", ""])
                for i in insights: summary_data.append([i, ""])
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False, header=False)

        if forecast_df is not None: forecast_df.to_excel(writer, sheet_name='Forecasts', index=False)
        if anomaly_df is not None: 
            anoms = anomaly_df[anomaly_df['Is_Anomaly'] == True]
            if not anoms.empty: anoms.to_excel(writer, sheet_name='Anomalies', index=False)
        if pivots:
            for name, pivot in pivots.items():
                pivot.to_excel(writer, sheet_name=name[:31].replace(':','').replace('/','_'))
    return buffer.getvalue()

def generate_markdown_report(df, pivots, forecast_df=None, anomaly_df=None, model_metrics=None, insights=None):
    """Generates Markdown report."""
    md = "# Analysis Report\n\n"
    md += f"- **Rows**: {len(df)}\n- **Columns**: {len(df.columns)}\n\n"
    
    if insights:
        md += "## Insights\n" + "\n".join([f"- {i}" for i in insights]) + "\n\n"
        
    if model_metrics:
        md += "## Model Metrics\n" + "\n".join([f"- **{k}**: {v}" for k, v in model_metrics.items()]) + "\n\n"
        
    if forecast_df is not None:
        md += "## Forecast\n" + forecast_df.head().to_markdown(index=False) + "\n\n"
        
    return md
