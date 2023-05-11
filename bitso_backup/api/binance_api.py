"""bitso_api"""

from typing import TypedDict, List, cast
import ccxt
from api.constants import API_KEY, API_SECRET_KEY
from api.config import get_exchange_config

binance_api = ccxt.binance()

public_api = ccxt.bitso(get_exchange_config())

private_api = ccxt.bitso(
    get_exchange_config(api_key=API_KEY, api_secret=API_SECRET_KEY)
)


class Precision(TypedDict):
    """Market Precision"""

    price: int  # integer or float for TICK_SIZE roundingMode
    amount: int  # integer, might be missing if not supplied by the exchange
    cost: int  # integer, very few exchanges actually have it


class Market(TypedDict):
    """https://docs.ccxt.com/#/README?id=markets"""

    symbol: str  # uppercase string literal of a pair of currencies
    base: str  # uppercase string, unified base currency code, 3 or more letters
    quote: str  # uppercase string, unified quote currency code, 3 or more letters
    baseId: str  # any string, exchange-specific base currency id
    quoteId: str  # any string, exchange-specific quote currency id
    precision: Precision  # number of decimal digits "after the dot"


def get_markets() -> List[Market] | None:
    """Get a list of all MXN available markets"""

    try:
        markets = public_api.fetch_markets()
    except (ccxt.NetworkError, ccxt.AuthenticationError, ccxt.ExchangeError):
        return None

    markets = cast(List[Market], markets)

    return [market for market in markets if market["quote"] == "MXN"]


def get_balance() -> object | None:
    """get account balance"""

    try:
        account_balance = private_api.fetch_balance()
    except (ccxt.NetworkError, ccxt.AuthenticationError, ccxt.ExchangeError):
        return None
    else:
        return account_balance


def initiate_websocket():
    print("websocket initiated")
