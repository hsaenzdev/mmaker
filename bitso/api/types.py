"""types"""

from typing import TypedDict, Any, Dict, List

GenericDict = Dict[str, Any]
ListOfDicts = List[GenericDict]
Payload = GenericDict | ListOfDicts


class ApiResponseError(TypedDict):
    """ApiResponseError"""
    message: str
    code: str


class ApiResponse(TypedDict):
    """ApiResponse"""
    success: bool
    payload: Payload
    error: ApiResponseError


class Book(TypedDict):
    """Book"""
    name: str
    value: int
