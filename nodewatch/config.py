import os

LOG_LEVEL = os.getenv("NODEWATCH_LOG_LEVEL", "INFO")
LOG_JSON = os.getenv("NODEWATCH_LOG_JSON", "true").lower() == "true"

API_HOST = os.getenv("NODEWATCH_API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("NODEWATCH_API_PORT", 8080))