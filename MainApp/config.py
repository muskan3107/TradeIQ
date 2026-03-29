import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Database
DATABASE_PATH = os.path.join(DATA_DIR, "portfolio.db")

# Cache & reports
CACHE_DIR = os.path.join(DATA_DIR, "cache")
REPORTS_DIR = os.path.join(DATA_DIR, "sample_reports")

# Model settings
MODEL_SETTINGS = {
    "model_name": "gpt-3.5-turbo",
    "temperature": 0.2,
    "max_tokens": 2048,
}

# Tool configurations
TOOL_CONFIG = {
    "document_processor": {
        "supported_formats": ["pdf", "txt", "html"],
        "max_file_size_mb": 20,
    },
    "metric_extractor": {
        "metrics": ["revenue", "net_income", "eps", "pe_ratio", "debt_to_equity"],
    },
    "sentiment_analyzer": {
        "threshold_positive": 0.6,
        "threshold_negative": 0.4,
    },
    "portfolio_manager": {
        "default_currency": "USD",
        "max_positions": 50,
    },
    "alert_scanner": {
        "check_interval_seconds": 300,
        "alert_channels": ["ui"],
    },
}
