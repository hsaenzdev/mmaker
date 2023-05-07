"""constants"""
import os

# ENV
ENVIRONMENT = os.environ.get("ENVIRONMENT", default="testing")

# API
API_KEY = os.environ.get("API_KEY", default="")
API_SECRET_KEY = os.environ.get("SECRET_KEY", default="")
API_TESTING_URL = os.environ.get("API_TESTING_URL", default="")
API_PRODUCTION_URL = os.environ.get("API_PRODUCTION_URL", default="")
BITSO_API_URL = API_TESTING_URL if ENVIRONMENT == "testing" else API_PRODUCTION_URL
