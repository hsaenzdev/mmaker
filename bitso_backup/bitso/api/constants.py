"""constants"""
import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", default="testing")
API_PRODUCTION_URL = os.environ.get("API_PRODUCTION_URL", default="")
API_TESTING_URL = os.environ.get("API_TESTING_URL", default="")
BITSO_API_URL = API_TESTING_URL if ENVIRONMENT == "testing" else API_PRODUCTION_URL
API_REQUEST_TIMEOUT = int(os.environ.get("API_REQUEST_TIMEOUT", 5))
BITSO_WEBSOCKET_URL = "wss://ws.bitso.com"
