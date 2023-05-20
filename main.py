from api.websocket import ThreadedWebsocket


tws = ThreadedWebsocket(symbol="BTCUSDT")

tws.on_trade = lambda price: print("ON_TRADE | trade price:", price["price"])

tws.on_order = lambda depth: print("ON_ORDER | best bid", depth["bids"][0])

tws.on_kline = lambda candle: print("ON_KLINE | Closed Price", candle["ClosePrice"])

tws.initiate_websocket()
