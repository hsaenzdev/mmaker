from api.websocket import ThreadedWebsocket


tws = ThreadedWebsocket(symbol="BTCUSDT")

# tws.on_trade = lambda price: print("trade price:", price["price"])

tws.on_order = lambda depth: print("best bid", depth["bids"][0])

tws.initiate_websocket()
