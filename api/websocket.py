from typing import Callable, TypedDict, List, Literal
import time
from binance import ThreadedWebsocketManager, Client
from constants import API_KEY, API_SECRET_KEY


class TradePayload(TypedDict):
    price: str
    buyer_order_id: int
    seller_order_id: int


class OrderBookPayload(TypedDict):
    bids: List[List[str]]
    asks: List[List[str]]


class ThreadedWebsocket:
    """https://python-binance.readthedocs.io/en/latest/websockets.html"""

    symbol: str
    websocket: ThreadedWebsocketManager

    # Message events
    on_trade: Callable[[TradePayload], None] | None = None
    on_order: Callable[[OrderBookPayload], None] | None = None
    on_kline: Callable | None = None

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def initiate_websocket(self):
        self.websocket = ThreadedWebsocketManager(
            api_key=API_KEY, api_secret=API_SECRET_KEY
        )

        self.websocket.start()

        self.websocket.start_kline_socket(
            callback=self.handle_kline_socket,
            symbol=self.symbol,
            interval=Client.KLINE_INTERVAL_15MINUTE,
        )

        self.websocket.start_trade_socket(
            symbol=self.symbol, callback=self.handle_trade_socket
        )

        self.websocket.start_depth_socket(
            symbol=self.symbol, callback=self.handle_depth_socket
        )

        self.websocket.join()

    def restart_websocket(self):
        """Restarts the websocket connection"""
        time.sleep(1)

        try:
            self.websocket.stop()
        except:
            pass

        self.initiate_websocket()

    def handle_message(
        self, message, event_type: Literal["trade", "kline", "depthUpdate"]
    ) -> bool:
        if "e" not in message:
            return False

        if message["e"] == "error":
            self.restart_websocket()
            return False

        return message["e"] == event_type

    def handle_depth_socket(self, message):
        if self.on_order is None:
            return

        if self.handle_message(message, "depthUpdate") is False:
            return

        if len(message["b"]) == 0 and len(message["a"]) == 0:
            return

        self.on_order(
            {
                "asks": message["a"],
                "bids": message["b"],
            }
        )

    def handle_trade_socket(self, message):
        if self.on_trade is None:
            return

        if self.handle_message(message, "trade") is False:
            return

        self.on_trade(
            {
                "price": message["p"],
                "buyer_order_id": message["b"],
                "seller_order_id": message["a"],
            }
        )

    def handle_kline_socket(self, message):
        if self.on_kline is None:
            return

        if self.handle_message(message, "kline") is False:
            return
