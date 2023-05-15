"""constants"""
import os

# ENV
ENVIRONMENT = os.environ.get("ENVIRONMENT", default="testing")

# API
API_KEY = os.environ.get("API_KEY", default="")
API_SECRET_KEY = os.environ.get("API_SECRET_KEY", default="")
