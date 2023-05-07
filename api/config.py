"""exchange config"""
from api.constants import BITSO_API_URL


def get_exchange_config(api_key: str | None = None, api_secret: str | None = None):
    """get exchange config"""

    rate_limit = 60 if api_key is None or api_secret is None else 300

    rate_limit_ms = 1000 / rate_limit

    return {
        "apiKey": api_key,
        "secret": api_secret,
        "rateLimit": rate_limit_ms,
        "urls": {
            "api": BITSO_API_URL,
            "www": "https://bitso.com",
            "doc": "https://docs.bitso.com/bitso-api/docs",
        },
    }
