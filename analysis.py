import pandas as pd
from scipy import stats

def detect_anomalies(df, column, threshold=2.5):
    """Detect anomalies using Z-score method"""
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return pd.Series([False] * len(df))
    
    z_scores = stats.zscore(df[column].dropna())
    anomalies = pd.Series([False] * len(df))
    anomalies[df[column].notna()] = abs(z_scores) > threshold
    return anomalies

def detect_anomalies_iqr(df, column, multiplier=1.5):
    """Detect anomalies using IQR method"""
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return pd.Series([False] * len(df))
    
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - (multiplier * IQR)
    upper_bound = Q3 + (multiplier * IQR)
    
    anomalies = (df[column] < lower_bound) | (df[column] > upper_bound)
    return anomalies

def analyze_trends(df):
    """Analyze trends in the dataset"""
    insights = []
    
    # Check if required columns exist
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
    
    # Revenue trends by region (if applicable)
    if 'region' in df.columns and 'revenue' in df.columns:
        region_trends = df.groupby('region')['revenue'].agg(['sum', 'mean', 'count'])
        insights.append({
            'type': 'region_performance',
            'data': region_trends
        })
    
    # Overall revenue trend
    if 'revenue' in df.columns:
        total_revenue = df['revenue'].sum()
        avg_revenue = df['revenue'].mean()
        insights.append({
            'type': 'overall_metrics',
            'total_revenue': total_revenue,
            'avg_revenue': avg_revenue
        })
    
    return insights

def aggregate_by_category(df, cat_col, num_col):
    """Aggregate data by category for visualization"""
    agg_df = df.groupby(cat_col)[num_col].agg(['sum', 'mean', 'count']).reset_index()
    agg_df = agg_df.sort_values('sum', ascending=False).head(15)
    return agg_df

def calculate_correlations(df, numeric_cols):
    """Calculate correlation matrix for numeric columns"""
    if len(numeric_cols) >= 2:
        return df[numeric_cols].corr()
    return None