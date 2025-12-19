import pandas as pd
import streamlit as st

def load_file(uploaded_file):
    """Load CSV or Excel file with error handling"""
    df = None
    if uploaded_file.name.endswith('.csv'):
        # Try multiple encodings to handle different CSV formats
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252', 'cp1252']
        last_error = None
        
        for encoding in encodings:
            try:
                uploaded_file.seek(0)  # Reset file pointer
                df = pd.read_csv(uploaded_file, encoding=encoding)
                st.success(f"Successfully loaded: {uploaded_file.name} (encoding: {encoding})")
                break
            except (UnicodeDecodeError, UnicodeError):
                last_error = f"Failed with encoding: {encoding}"
                continue
            except Exception as e:
                last_error = str(e)
                break
        
        if df is None:
            raise Exception(f"Could not read CSV file. Last error: {last_error}")
    else:
        df = pd.read_excel(uploaded_file)
        st.success(f"Successfully loaded: {uploaded_file.name}")
    return df

def load_sample_data():
    """Load the built-in sample data"""
    return pd.read_csv("sample_retail_data.csv")

def detect_column_types(df):
    """Identify numeric, date, and categorical columns"""
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    date_cols = []
    categorical_cols = []
    
    # Try to detect date columns
    for col in df.columns:
        if col.lower() in ['date', 'datetime', 'timestamp', 'invoicedate', 'orderdate', 'time']:
            try:
                pd.to_datetime(df[col])
                date_cols.append(col)
            except:
                pass
    
    # Detect categorical columns
    for col in df.columns:
        if col not in numeric_cols and col not in date_cols:
            if df[col].nunique() < 50 and df[col].nunique() > 1:
                categorical_cols.append(col)
                
    return numeric_cols, date_cols, categorical_cols

def get_date_range_info(df):
    """Get formatted date range string if date column exists"""
    if 'date' in df.columns:
        try:
            df_temp = df.copy()
            df_temp['date'] = pd.to_datetime(df_temp['date'])
            return f"\n- Date Range: {df_temp['date'].min()} to {df_temp['date'].max()}"
        except:
            pass
    return ""
