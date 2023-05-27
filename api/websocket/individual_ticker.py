from typing import Callable, TypedDict, List, Literal
from api.websocket.tws import tws


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


class IndividualTicker:
    """https://python-binance.readthedocs.io/en/latest/websockets.html"""

    symbol: str
    # websocket: ThreadedWebsocketManager

    on_trade: Callable[[TradePayload], None] | None = None
    on_order: Callable[[OrderBookPayload], None] | None = None
    on_kline: Callable[[KlinePayload], None] | None = None

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

        print(tws.test_var)
        tws.test_var = "VAR002 - ALV"

    def initiate_depth(self, symbol) -> None:
        tws.websocket.start_depth_socket(
            symbol=symbol, callback=self.handle_depth_socket
        )

    def handle_message(self, message, event_type: EventType) -> bool:
        if "e" not in message:
            return False

        if message["e"] == "error":
            tws.restart_websocket()
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
