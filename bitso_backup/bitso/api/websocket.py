"""web"""
import asyncio
import json
from typing import List, Callable, TypedDict, Literal, cast
import websockets.client
import websockets.exceptions
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    WebSocketException,
)

from bitso.api.constants import BITSO_WEBSOCKET_URL

ChannelType = Literal["orders", "trades"]


class Order(TypedDict):
    """Websocket order"""

    a: str  # The amount
    d: int  # Unix timestamp
    o: str  # Order ID
    r: str  # The rate
    s: str  # The status. Set to undefined by default.
    t: int  # 0 indicates buy | 1 indicates sell
    v: str  # The value


class OrdersPayload(TypedDict):
    """Websocket orders payload"""

    bids: List[Order]
    asks: List[Order]


class TradesPayload(TypedDict):
    """Websocket trade"""

    a: str  # The amount
    i: int  # A number that uniquely identifies the transaction
    mo: str  # Maker Order ID
    r: str  # The rate
    t: int  # 0 indicates buy | 1 indicates sell
    to: str  # Taker Order ID
    v: str  # The value
    x: int  # Creation timestamp


class WebSocketMessage(TypedDict):
    """Websocket message"""

    type: ChannelType
    book: str
    payload: OrdersPayload | TradesPayload
    sent: float


OnTradesCallBack = Callable[[TradesPayload], None] | None
OnOrdersCallBack = Callable[[OrdersPayload], None] | None


class BitsoWebSocket:
    """Bitso websocket"""

    def __init__(
        self,
        on_orders: OnOrdersCallBack = None,
        on_trades: OnTradesCallBack = None,
    ):
        self.websocket = None
        self.on_orders = on_orders
        self.on_trades = on_trades

    def on_message(self, message: WebSocketMessage) -> None:
        """Bitso websocket message received"""

        if "payload" not in message or "type" not in message:
            return

        if message["type"] == "orders" and self.on_orders is not None:
            orders_payload = cast(OrdersPayload, message["payload"])

            self.on_orders(orders_payload)

        elif message["type"] == "trades" and self.on_trades is not None:
            trades_payload = cast(TradesPayload, message["payload"])

            self.on_trades(trades_payload)

    async def connect(self, retry_delay: int = 15) -> None:
        """Connection to the bitso websocket"""

        while True:
            try:
                async with websockets.client.connect(BITSO_WEBSOCKET_URL) as websocket:
                    await self.subscribe(websocket, "orders")
                    await self.handle_messages(websocket)
            except (ConnectionClosedError, ConnectionClosedOK):
                print(f"Connection lost. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            except WebSocketException:
                print(f"retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)

    async def subscribe(self, websocket, channel_type: ChannelType) -> None:
        subscription_message = json.dumps(
            {"action": "subscribe", "book": "xrp_mxn", "type": channel_type}
        )
        await websocket.send(subscription_message)

    async def handle_messages(self, websocket) -> None:
        async for message in websocket:
            data = json.loads(message)
            self.on_message(data)
