import time
from binance import ThreadedWebsocketManager
from constants import API_KEY, API_SECRET_KEY


class _ThreadedWebsocket:
    websocket: ThreadedWebsocketManager

    test_var: str = "VALUE001"

    def __init__(self) -> None:
        self.websocket = ThreadedWebsocketManager(
            api_key=API_KEY, api_secret=API_SECRET_KEY
        )

        self.initiate_websocket()

    def initiate_websocket(self) -> None:
        self.websocket.start()

    def restart_websocket(self) -> None:
        """Restarts the websocket connection"""
        try:
            self.websocket.stop()
        except:
            pass

        time.sleep(15)

        self.initiate_websocket()


tws = _ThreadedWebsocket()
