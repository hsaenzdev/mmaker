"""Hello world"""
import api

# import asyncio
# from bitso.api.get_available_books import get_available_books
# from bitso.api.websocket import BitsoWebSocket
# from bitso.api.websocket import OrdersPayload

# books = get_available_books()

# if books:
#     print(books[0]["book"], books[0]["default_chart"])


# def handle_websocket_orders(orders: OrdersPayload):
#     """callback test"""
#     print(orders["asks"][0]["o"], orders["bids"][0]["r"])


# async def main() -> None:
#     bitso_ws = BitsoWebSocket(on_orders=handle_websocket_orders)

#     await bitso_ws.connect()


# if __name__ == "__main__":
#     asyncio.run(main())
