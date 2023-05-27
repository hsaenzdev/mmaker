import time
from binance import ThreadedWebsocketManager
from constants import API_KEY, API_SECRET_KEY


def to_number(string):
    try:
        number = int(string)
        return number
    except ValueError:
        try:
            number = float(string)
            return number
        except ValueError:
            return 0


class AllMarketTickers:
    """https://python-binance.readthedocs.io/en/latest/websockets.html"""

    websocket: ThreadedWebsocketManager

    def __init__(self) -> None:
        self.websocket = ThreadedWebsocketManager(
            api_key=API_KEY, api_secret=API_SECRET_KEY
        )

    def initiate_websocket(self) -> None:
        self.websocket.start()

        self.websocket.start_ticker_socket(callback=self.handle_ticker)

        self.websocket.join()

    def restart_websocket(self) -> None:
        """Restarts the websocket connection"""
        try:
            self.websocket.stop()
        except:
            pass

        time.sleep(15)

        self.initiate_websocket()

    def handle_ticker(self, message) -> None:
        if len(message) == 0:
            return

        # Only USDT
        usdt_ticker = [d for d in message if str(d["s"]).endswith("USDT")]

        # +1 24h change
        usdt_ticker = [d for d in usdt_ticker if to_number(d["P"]) > 0]

        # More traded volume
        usdt_ticker = sorted(
            usdt_ticker, key=lambda d: to_number(d["v"]), reverse=True
        )[:10]

        print(usdt_ticker[0])
