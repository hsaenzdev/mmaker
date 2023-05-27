import time
from api.websocket.individual_ticker import IndividualTicker


def main():
    individual_ticker_process("BTCUSDT")

    time.sleep(10)

    print("next tick")
    individual_ticker_process("XRPUSDT")

    while True:
        print("this keep running")
        time.sleep(60)


def individual_ticker_process(symbol: str):
    ist = IndividualTicker(symbol=symbol)

    ist.on_order = lambda order: print(
        order["asks"][0] if len(order["asks"]) > 0 else 0
    )

    ist.initiate_depth(symbol)

    time.sleep(5)
    ist.initiate_depth(symbol)


if __name__ == "__main__":
    main()
