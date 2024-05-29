"""Error handling for the TextEmbed API."""

from __future__ import annotations

from typing import Optional

from fastapi import Request
from fastapi.responses import ORJSONResponse


class EmbeddingException(Exception):
    """Custom exception class for embedding-related errors.

    Args:
        message (str): Description of the error.
        code (int): HTTP status code associated with the error.
        type (Optional[str], optional): Type of error. Defaults to None.
        param (Optional[str], optional): Parameter related to the error, if any. Defaults to None.
    """

    def __init__(
        self,
        message: str,
        code: int,
        exc_type: Optional[str] = None,
        param: Optional[str] = None,
    ):
        self.message = message
        self.exc_type = exc_type
        self.param = param
        self.code = code

    def json(self) -> dict:
        """Converts the exception details to a JSON-serializable dictionary.

        Returns:
            dict: Dictionary containing error details.
        """
        return {
            "error": {
                "message": self.message,
                "type": self.exc_type,
                "param": self.param,
                "code": self.code,
            }
        }


def embedding_exception_handler(
    request: Request, exc: EmbeddingException
) -> ORJSONResponse:
    """Exception handler for EmbeddingException, returning a JSON response.

    Args:
        request (Request): The incoming request object.
        exc (EmbeddingException): The raised exception instance.

    Returns:
        ORJSONResponse: JSON response containing error details and the appropriate HTTP status code.
    """
    return ORJSONResponse(
        status_code=exc.code,
        content=exc.json(),
    )
