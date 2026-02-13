import pandas as pd

def generate_pivot_tables(df, numeric_cols, categorical_cols, date_cols):
    """Generates pivot tables."""
    pivots = {}
    
    # Cat vs Numeric
    for cat_col in categorical_cols[:3]:
        if df[cat_col].nunique() > 50: continue
        try:
            pivot = df.pivot_table(index=cat_col, values=numeric_cols, aggfunc='sum')
            pivots[f"{cat_col}_summary"] = pivot
        except Exception: pass
            
    # Date Trends
    for date_col in date_cols:
        try:
            pivot = df.pivot_table(index=date_col, values=numeric_cols, aggfunc='sum')
            pivots[f"{date_col}_trend"] = pivot
        except Exception: pass
            
    return pivots
