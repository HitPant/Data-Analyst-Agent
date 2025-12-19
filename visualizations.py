import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_time_series_chart(df, date_col, numeric_col, cat_col=None):
    """Create a time series line chart"""
    df_viz = df.copy()
    df_viz[date_col] = pd.to_datetime(df_viz[date_col])
    df_viz = df_viz.sort_values(date_col)
    
    if cat_col:
        # Limit to top 10 categories to avoid clutter
        top_categories = df_viz[cat_col].value_counts().head(10).index
        df_viz_filtered = df_viz[df_viz[cat_col].isin(top_categories)]
        
        fig = px.line(df_viz_filtered, x=date_col, y=numeric_col, color=cat_col,
                        title=f"{numeric_col} Trends by {cat_col}")
    else:
        fig = px.line(df_viz, x=date_col, y=numeric_col,
                        title=f"{numeric_col} Over Time")
    return fig

def create_distribution_chart(df, numeric_col):
    """Create a histogram for distribution analysis"""
    fig = px.histogram(df, x=numeric_col, nbins=50,
                        title=f"Distribution of {numeric_col}")
    return fig

def create_categorical_bar_chart(agg_df, cat_col, num_col):
    """Create a bar chart for categorical aggregation"""
    fig = px.bar(agg_df, x=cat_col, y='sum',
                title=f"Total {num_col} by {cat_col}",
                color='sum',
                color_continuous_scale='Blues')
    return fig

def create_correlation_heatmap(corr_matrix):
    """Create a correlation heatmap"""
    fig = px.imshow(corr_matrix, 
                    text_auto=True,
                    aspect="auto",
                    title="Correlation Between Numeric Variables",
                    color_continuous_scale='RdBu_r')
    return fig

def create_anomaly_scatter_chart(df, col, anomaly_indices):
    """Create a scatter plot highlighting anomalies"""
    fig = px.scatter(df, y=col, title=f"{col} - Anomaly Detection")
    fig.add_scatter(
        y=df.loc[anomaly_indices, col],
        mode='markers',
        marker=dict(size=12, color='red'),
        name='Anomalies'
    )
    return fig
