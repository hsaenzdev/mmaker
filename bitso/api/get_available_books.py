"""
List Available Books
https://docs.bitso.com/bitso-api/docs/list-available-books
"""

from typing import List, TypedDict, cast
from bitso.api.bitso_request import make_bitso_request


class FlatRate(TypedDict):
    """
    Acts as a fallback mechanism that specifies the fees
    to apply to makers and takers in case a fee structure is not defined for the book.
    """

    maker: str
    taker: str


class Structure(TypedDict):
    """
    Describes the fee tiers defined based on the volume traded.
    For example, in the payload shown, the first tier goes from 0 to 1,500,000,
    the second from 1,500,001 to 2,000,000, and so forth.
    Increasing your trading volume lowers fees only if it reaches the next tier.
    Every tier shows the fee applied to makers and takers as a decimal,
    and the volume figures reported are denominated in the minor currency.
    """

    volume: str
    maker: str
    taker: str


class Fees(TypedDict):
    """The fee structure applied in the book. See the table below for its description."""

    flat_rate: FlatRate
    structure: List[Structure]


class AvailableBooks(TypedDict):
    """Available books payload"""

    book: str
    default_chart: str
    fees: Fees
    minimum_amount: str
    maximum_amount: str
    minimum_price: str
    maximum_price: str
    minimum_value: str
    maximum_value: str
    tick_size: str


def get_available_books() -> List[AvailableBooks] | None:
    """
    Fetch available_books from Bitso API.

    This function makes a request to the Bitso API to retrieve the available_books
    and returns the list of available books with their respective details.
    If the request fails or the payload is not available, the function returns None.

    Returns:
        List[AvailableBooks] | None: A list of available books with their details,
        or None if the request fails.
    """

    payload = make_bitso_request(path="available_books")

    if payload is not None:
        return cast(List[AvailableBooks], payload)

    return None
