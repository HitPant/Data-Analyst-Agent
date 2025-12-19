# AI Data Analyst

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Google Cloud Project with the Gemini API enabled
- An API Key for the Gemini API

### Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/HitPant/Data-Analyst-Agent.git
   cd Data-Analyst-Agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

### Running the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

---

# AI Data Analyst - Project Overview

This project is a Streamlit-based application designed to perform automated data analysis on retail sales datasets. It leverages statistical methods for anomaly detection and Google's Gemini AI for generating qualitative business insights. 

## Key Concepts & Methodology

### Anomaly Detection
The system uses statistical methods to automatically spot unusual data points (outliers).
- **Z-Score (Standard deviation)**: 
    - **What**: Measures how many standard deviations a data point is away from the mean.
    - **Why**: Best for finding outliers in data that follows a normal "bell-curve" distribution.
- **IQR (Interquartile Range)**:
    - **What**: Focuses on the middle 50% of the data ranges.
    - **Why**: effective for skewed data (like sales) that doesn't follow a perfect bell curve.

### Automated Analysis
The system performs several layers of analysis automatically:
- **Trend Analysis**: Groups data by time or region to show performance direction (Growth vs Decline).
- **Correlation**: mathematically checks if two variables move together (e.g., "Do higher discounts lead to higher sales?").
- **Categorical Aggregation**: Summarizes performance by product type, region, or segment.

### Smart Data Processing
The data processing engine handles the messy work of data ingestion:
- **Robust Loading**: Automatically detects and handles different file encodings (UTF-8, Latin-1, etc.) and formats (CSV, Excel).
- **Type Intelligence**: Automatically categorizes columns into **Numeric** (for stats), **Time-series** (for trends), and **Categorical** (for segmentation) without user setup.
- **Safety Checks**: Validates data structure to prevent crashes before analysis begins.



## Assumptions

1. **Data Structure**:
   - The dataset must contain **at least one numeric column** for statistical analysis and anomaly detection.
   - This project is designed to analyze **Retail Sales Data** and similar time-series datasets.
   - It expects a **Date column** for trend analysis and **Categorical columns** (like Product Category or Region) for segmentation.

2. **Anomaly Detection**:
   - Supports two robust methods:
     - **Z-Score**: Best for normally distributed data. Configurable sensitivity threshold (Default: 2.5).
     - **Interquartile Range (IQR)**: Best for skewed data (e.g., sales spikes). Configurable multiplier (Default: 1.5).



## Sample Output

The application generates a comprehensive dashboard containing:

1. **Data Preview & Health**: Quick summary of rows, columns, and date ranges.
2. **Statistical Overview**: Standard descriptive statistics (mean, min, max, std dev).
3. **Anomaly Report**:
   - Interactive scatter plots highlighting outliers in red.
   - Filtered data tables showing specific anomalous records.
4. **Visualizations**:
   - **Time Series**: Revenue/Sales trends over time, color-coded by category.
   - **Distribution**: Histograms showing the spread of numeric variables.
   - **Correlation Heatmap**: Visual grid of relationships between metrics.
5. **AI Business Report**:
   - **Executive Summary**: High-level sales performance.
   - **Key Trends**: Growth/decline patterns.
   - **Anomalies**: Business context for detected outliers.
   - **Recommendations**: 2-3 actionable steps based on the data.
