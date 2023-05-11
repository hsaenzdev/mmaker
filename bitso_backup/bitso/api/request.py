"""Bitso request"""
from typing import cast
from urllib.parse import urljoin
from requests import get, Response
from requests.exceptions import RequestException, Timeout, TooManyRedirects

from bitso.api.types import ApiResponse, Payload
from bitso.api.constants import BITSO_API_URL, API_REQUEST_TIMEOUT


def handle_api_error(message="Unknown"):
    """handle api error"""
    print("Error captured:")
    print(message)


def handle_api_response(response: Response) -> Payload | None:
    """handle_api_response"""

    api_response = cast(ApiResponse, response.json())

    if api_response["success"]:
        return api_response["payload"]

    handle_api_error(api_response["error"]["message"])

    return None


def make_bitso_request(path: str) -> Payload | None:
    """fetch"""

    url = urljoin(BITSO_API_URL, path)

    try:
        response = get(url, timeout=API_REQUEST_TIMEOUT)
        response.raise_for_status()

        return handle_api_response(response)
    except Timeout:
        return handle_api_error("timeout error")
    except TooManyRedirects:
        return handle_api_error("too many request")
    except RequestException as error:
        return handle_api_error(str(error))
