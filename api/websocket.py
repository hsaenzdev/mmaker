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


class KlinePayload(TypedDict):
    OpenPrice: str
    ClosePrice: str
    HightPrice: str
    LowPrice: str


EventType = Literal["trade", "kline", "depthUpdate"]


class ThreadedWebsocket:
    """https://python-binance.readthedocs.io/en/latest/websockets.html"""

    symbol: str
    websocket: ThreadedWebsocketManager

    on_trade: Callable[[TradePayload], None] | None = None
    on_order: Callable[[OrderBookPayload], None] | None = None
    on_kline: Callable[[KlinePayload], None] | None = None

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

        self.websocket = ThreadedWebsocketManager(
            api_key=API_KEY, api_secret=API_SECRET_KEY
        )

    def initiate_websocket(self) -> None:
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

    def restart_websocket(self) -> None:
        """Restarts the websocket connection"""
        try:
            self.websocket.stop()
        except:
            pass

        time.sleep(15)

        self.initiate_websocket()

    def handle_message(self, message, event_type: EventType) -> bool:
        if "e" not in message:
            return False

        if message["e"] == "error":
            self.restart_websocket()
            return False

        return message["e"] == event_type

    def handle_depth_socket(self, message) -> None:
        if self.on_order is None:
            return

        if self.handle_message(message, "depthUpdate") is False:
            return

        self.on_order(
            {
                "asks": message["a"],
                "bids": message["b"],
            }
        )

    def handle_trade_socket(self, message) -> None:
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

    def handle_kline_socket(self, message) -> None:
        if self.on_kline is None:
            return

        if self.handle_message(message, "kline") is False:
            return

        self.on_kline(
            {
                "OpenPrice": message["k"]["o"],
                "ClosePrice": message["k"]["c"],
                "HightPrice": message["k"]["h"],
                "LowPrice": message["k"]["l"],
            }
        )
