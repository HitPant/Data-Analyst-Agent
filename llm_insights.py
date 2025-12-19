import google.generativeai as genai
import config

def generate_ai_insights(df, anomalies_summary, trends, api_key):
    """Generate insights using Gemini AI"""
    
    if not api_key:
        return "Please configure your Gemini API key to get AI-powered insights."
    
    # Configure API
    genai.configure(api_key=api_key)
    
    try:
        # Prepare data summary
        date_range_info = ""
        if 'date' in df.columns:
            # Note: We duplicate simple invalid check here or pass pre-computed info
            # relying on what's passed or simple re-computation
             pass 

        # We need to construct the summary string. 
        # Ideally this logic matches what was in app.py
        
        data_summary = f"""
Dataset Overview:
- Total Records: {len(df)}
- Columns: {', '.join(df.columns.tolist())}

Key Statistics:
{df.describe().to_string()}

Anomalies Detected:
{anomalies_summary}

Recent Data Sample:
{df.tail(10).to_string()}
"""
        
        # Create prompt for Gemini
        prompt = f"""You are a senior data analyst for a retail company. Analyze the following sales dataset and provide a structured, executive-level business analysis.

IMPORTANT FORMATTING RULES:
- Format your response in clean, readable markdown.
- Use DOUBLE NEWLINES between all sections and paragraphs to ensure proper rendering.
- Ensure bullet points are properly spaced from the text above them.

IMPORTANT CONTENT RULES:
- Use a professional, non-technical business tone (avoid filler words).
- Quantify EVERY insight (e.g., "Revenue grew by 15%", "North region contributes 60% of sales"). DO NOT perform complex new calculations, but interpret the provided metrics and trends.
- Limit specific recommendations to exactly 2-3 high-impact actions.

Provide the following sections in strict markdown format:

1. **Top 3 Key Insights**
   - Provide the 3 most critical findings.
   - Must be quantitative and business-focused.

2. **Trends Identified**
   - Highlight key patterns (seasonality, growth, decline).
   - Support with specific data points from the summary.

3. **Anomalies Explanation**
   - Briefly explain the significance of any anomalies detected (or state "No significant anomalies" if none).
   - Assess if they represent a risk or opportunity.

4. **Data Assumptions & Limitations**
   - Briefly acknowledge constraints (e.g., "Analysis based on limited sample," "Seasonality may be affected by short timeframe").
   - Mention that anomalies are statistically derived and require verification.

5. **Recommended Actions**
   - Provide EXACTLY 2-3 actionable, prioritized steps.
   - Link each recommendation to a specific insight from above.

{data_summary}

Please provide a clear, concise, and PROPERLY FORMATTED business analysis with correct spacing and punctuation."""

        # Call Gemini API
        model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)
        
        response = model.generate_content(
            prompt,
            generation_config={'temperature': config.GEMINI_TEMPERATURE}
        )
        
        # Return the response text, escaping dollar signs to prevent LaTeX formatting
        return response.text.replace('$', '\\$')
    
    except Exception as e:
        return f"Error generating insights: {str(e)}\n\nPlease check your API key and internet connection."