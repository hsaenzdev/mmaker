"""Hello world"""

from bitso.api.get_available_books import get_available_books

books = get_available_books()

if books:
    print(books[0]["book"], books[0]["default_chart"], books[0]["fees"])
else:
    print("An error happen")
