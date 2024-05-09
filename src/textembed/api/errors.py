from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from fastapi import Request
from fastapi.responses import ORJSONResponse


class OpenAIException(Exception):
    """An exception in OpenAI Style"""

    def __init__(
        self,
        message: str,
        code: int,
        type: Optional[str] = None,
        param: Optional[str] = None,
    ):
        self.message = message
        self.type = type
        self.param = param
        self.code = code

    def json(self):
        return {
            "error": {
                "message": self.message,
                "type": self.type,
                "param": self.param,
                "code": self.code,
            }
        }


def openai_exception_handler(request: Request, exc: OpenAIException):
    return ORJSONResponse(
        status_code=exc.code,
        content=exc.json(),
    )
