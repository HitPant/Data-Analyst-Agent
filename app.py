import streamlit as st
import google.generativeai as genai
import config
import data_processing
import analysis
import visualizations
import llm_insights

# Configure page
st.set_page_config(
    page_title=config.PAGE_TITLE,
    layout=config.LAYOUT
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Title and description
    st.title("AI Data Analyst")
    st.markdown("Upload your sales data and get automated insights, trend analysis, and actionable recommendations.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key handling
        if config.GEMINI_API_KEY:
             st.success("API Key Loaded")
             api_key = config.GEMINI_API_KEY
        else:
            api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key")
        
        st.divider()
        
        # Anomaly detection settings
        # Anomaly detection settings
        st.subheader("Anomaly Detection")
        
        anomaly_method = st.selectbox(
            "Method",
            ["Z-Score", "IQR"],
            help="Z-Score: Good for normal distributions\nIQR: Good for skewed data (e.g. sales)"
        )
        
        if anomaly_method == "Z-Score":
            threshold = st.slider(
                "Z-Score Threshold", 
                config.MIN_Z_THRESHOLD, 
                config.MAX_Z_THRESHOLD, 
                config.DEFAULT_Z_THRESHOLD, 
                config.STEP_Z_THRESHOLD,
                help="Higher values = fewer anomalies detected"
            )
        else: # IQR
            threshold = st.slider(
                "IQR Multiplier",
                1.0,
                3.0,
                1.5,
                0.1,
                help="Higher values = fewer anomalies detected (1.5 is standard)"
            )
        
        st.divider()
        st.markdown("### 📖 About")
        st.info("This AI-powered tool analyzes retail sales data to identify trends, anomalies, and provide actionable insights.")

    # Main Content
    # File upload
    st.header("Upload Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file", 
        type=['csv', 'xlsx', 'xls'],
        help="Upload your sales data in CSV or Excel format"
    )
    
    # Use sample data button
    use_sample = st.button("Use Sample Data")
    
    df = None
    
    # Data Loading Logic
    if uploaded_file is not None:
        try:
            df = data_processing.load_file(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            
    elif use_sample:
        try:
            df = data_processing.load_sample_data()
            st.success("Sample data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading sample data: {str(e)}")
    
    # Process and display data
    if df is not None:
        st.divider()
        
        # --- Data Preview ---
        st.header("Data Preview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            # Check for date column logic
            date_info = data_processing.get_date_range_info(df)
            # Re-calculating periods just for the metric display as it was in original
            if 'date' in df.columns:
                 # We recreate the period count logic here or move to data_processing. 
                 # To keep it simple, we can do it here or call a helper.
                 # Original: len(pd.to_datetime(df['date']).unique())
                 import pandas as pd # Local import for this specific logic if needed
                 st.metric("Date Range", f"{len(pd.to_datetime(df['date']).unique())} periods")
        
        st.dataframe(df.head(10), use_container_width=True)
        
        # --- Basic Statistics ---
        st.header("Basic Statistics")
        st.dataframe(df.describe(), use_container_width=True)
        
        # --- Anomaly Detection ---
        st.header("🔍 Anomaly Detection")
        
        numeric_columns, date_cols, categorical_cols = data_processing.detect_column_types(df)
        
        anomalies_summary = "No numeric columns available"
        
        if numeric_columns:
            anomaly_results = {}
            for col in numeric_columns:
                if anomaly_method == "Z-Score":
                    anomalies = analysis.detect_anomalies(df, col, threshold)
                else:
                    anomalies = analysis.detect_anomalies_iqr(df, col, threshold)
                    
                anomaly_count = anomalies.sum()
                if anomaly_count > 0:
                    anomaly_results[col] = {
                        'count': anomaly_count,
                        'indices': df[anomalies].index.tolist()
                    }
            
            if anomaly_results:
                st.warning(f"Detected anomalies in {len(anomaly_results)} column(s)")
                
                for col, result in anomaly_results.items():
                    with st.expander(f"{col}: {result['count']} anomalies detected"):
                        anomaly_df = df.loc[result['indices']]
                        st.dataframe(anomaly_df, use_container_width=True)
                        
                        # Visualize anomalies
                        fig = visualizations.create_anomaly_scatter_chart(df, col, result['indices'])
                        st.plotly_chart(fig, use_container_width=True)
                
                anomalies_summary = "\n".join([f"- {col}: {result['count']} anomalies" for col, result in anomaly_results.items()])
            else:
                st.success("No significant anomalies detected")
                anomalies_summary = "No anomalies detected"
        else:
            st.info("No numeric columns found for anomaly detection")
        
        # --- Visualizations ---
        st.header("📊 Visualizations")
        
        viz_created = False
        
        # 1. Time series visualization
        if date_cols and numeric_columns:
            date_col = date_cols[0]
            numeric_col = numeric_columns[0]
            cat_col = categorical_cols[0] if categorical_cols else None
            
            fig = visualizations.create_time_series_chart(df, date_col, numeric_col, cat_col)
            st.plotly_chart(fig, use_container_width=True)
            viz_created = True
        
        # 2. Distribution
        if numeric_columns:
            selected_numeric = st.selectbox("Select numeric column for distribution", numeric_columns)
            fig = visualizations.create_distribution_chart(df, selected_numeric)
            st.plotly_chart(fig, use_container_width=True)
            viz_created = True
        
        # 3. Categorical analysis
        if categorical_cols and numeric_columns:
            col1, col2 = st.columns(2)
            
            with col1:
                cat_col = st.selectbox("Select category", categorical_cols)
            with col2:
                num_col = st.selectbox("Select value", numeric_columns)
            
            agg_df = analysis.aggregate_by_category(df, cat_col, num_col)
            fig = visualizations.create_categorical_bar_chart(agg_df, cat_col, num_col)
            st.plotly_chart(fig, use_container_width=True)
            viz_created = True
        
        # 4. Correlation heatmap
        if len(numeric_columns) >= 2:
            st.subheader("Correlation Heatmap")
            corr_matrix = analysis.calculate_correlations(df, numeric_columns)
            if corr_matrix is not None:
                fig = visualizations.create_correlation_heatmap(corr_matrix)
                st.plotly_chart(fig, use_container_width=True)
                viz_created = True
        
        if not viz_created:
            st.info("No suitable columns found for visualization.")
        
        # --- AI-Powered Insights ---
        st.header("AI-Powered Insights")
        
        if st.button("Generate Insights", type="primary"):
            with st.spinner("Analyzing data with Gemini AI..."):
                trends = analysis.analyze_trends(df)
                insights = llm_insights.generate_ai_insights(df, anomalies_summary, trends, api_key)
                
                st.markdown("### Analysis Results")
                st.markdown(insights)
                
    else:
        # Welcome screen
        st.info("Upload a dataset or use the sample data to get started!")
        st.markdown("""
        ### How it works:
        1. **Upload** your CSV or Excel file (or use sample data)
        2. **Review** automatic data analysis and statistics
        3. **Detect** anomalies using statistical methods
        4. **Visualize** trends with interactive charts
        5. **Get** AI-powered insights and recommendations
        """)

if __name__ == "__main__":
    main()
