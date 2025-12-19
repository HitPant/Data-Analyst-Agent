import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# App Config
PAGE_TITLE = "AI Data Analyst"
LAYOUT = "wide"

# Anomaly Detection Defaults
DEFAULT_Z_THRESHOLD = 2.5
MIN_Z_THRESHOLD = 1.5
MAX_Z_THRESHOLD = 4.0
STEP_Z_THRESHOLD = 0.1

# AI Model
GEMINI_MODEL_NAME = 'gemini-2.5-flash'
GEMINI_TEMPERATURE = 0.7
