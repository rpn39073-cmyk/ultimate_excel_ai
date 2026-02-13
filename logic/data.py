import pandas as pd
import numpy as np
import os
import io

def load_data(file_content, filename):
    """
    Loads data from bytes or file-like object.
    Returns a pandas DataFrame and a status message.
    """
    try:
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext == '.csv':
            df = pd.read_csv(file_content)
        elif file_ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_content)
        else:
            return None, "Unsupported file format. Please upload .csv or .xlsx."
            
        if df.empty:
            return None, "File is empty."
            
        return df, "Success"
        
    except Exception as e:
        return None, f"Error loading file: {str(e)}"

def clean_column_names(df):
    """Standardizes column names to snake_case."""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^\w]', '', regex=True)
    return df

def detect_column_types(df):
    """Detects numeric, categorical, and date columns."""
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass
                
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    return numeric_cols, categorical_cols, date_cols

def clean_missing_values(df, numeric_cols, categorical_cols):
    """Imputes missing values."""
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)
            
    for col in categorical_cols:
        if df[col].isnull().any():
            if not df[col].mode().empty:
                df[col].fillna(df[col].mode()[0], inplace=True)
            else:
                df[col].fillna("Unknown", inplace=True)
    return df

def remove_duplicates(df):
    """Removes duplicate rows."""
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    return df, duplicates_removed

def process_data(df):
    """
    Main processing pipeline.
    Returns cleaned dataframe, column types, and cleaning stats.
    """
    stats = {}
    df = clean_column_names(df)
    numeric_cols, categorical_cols, date_cols = detect_column_types(df)
    df, dups = remove_duplicates(df)
    stats['duplicates_removed'] = dups
    
    missing_before = df.isnull().sum().sum()
    df = clean_missing_values(df, numeric_cols, categorical_cols)
    stats['missing_filled'] = missing_before - df.isnull().sum().sum()
    
    return df, numeric_cols, categorical_cols, date_cols, stats
