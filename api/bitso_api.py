"""bitso_api"""

import ccxt
from api.constants import API_KEY, API_SECRET_KEY
from api.config import get_exchange_config

public_api = ccxt.bitso(get_exchange_config())

private_api = ccxt.bitso(
    get_exchange_config(api_key=API_KEY, api_secret=API_SECRET_KEY)
)
