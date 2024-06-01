"""Error handling for the TextEmbed API."""

from __future__ import annotations

from typing import Optional

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from textembed.log import logger


class EmbeddingException(Exception):
    """Custom exception class for embedding-related errors.

    Args:
        message (str): Description of the error.
        status_code (int): HTTP status code associated with the error.
        type (Optional[str], optional): Type of error. Defaults to None.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        exc_type: Optional[str] = None,
    ):
        self.message = message
        self.exc_type = exc_type
        self.status_code = status_code

    def json(self) -> dict:
        """Converts the exception details to a JSON-serializable dictionary.

        Returns:
            dict: Dictionary containing error details.
        """
        return {
            "message": self.message,
            "exc_type": self.exc_type,
            "status_code": self.status_code,
        }


class ModelNotFoundException(EmbeddingException):
    """Custom exception for model not found errors."""

    def __init__(self, message: str = "Model not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND, exc_type="ModelNotFound")


class HandleExceptions:
    """Handle Exceptions"""

    def __init__(self, app):
        self.app = app
        self._handle_custom_exception()
        self._handle_model_not_found_exception()
        self._handle_pydantic_exception()
        self._handle_fastapi_http_exception()
        self._handle_default_exception()

    def _handle_custom_exception(self):
        @self.app.exception_handler(EmbeddingException)
        async def custom_exception_handler(request: Request, exc: EmbeddingException):
            logger.error(exc.message)
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.json(),
            )

    def _handle_model_not_found_exception(self):
        @self.app.exception_handler(ModelNotFoundException)
        async def model_not_found_exception_handler(
            request: Request, exc: ModelNotFoundException
        ):
            logger.error(exc.message)
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.json(),
            )

    def _handle_pydantic_exception(self):
        @self.app.exception_handler(RequestValidationError)
        async def pydantic_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            logger.error("Pydantic Validation Error: %s", exc.errors())
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "message": "Validation error occurred",
                    "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                },
            )

    def _handle_fastapi_http_exception(self):
        @self.app.exception_handler(HTTPException)
        async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
            logger.error("FastAPI HTTP Exception: %s", exc.detail)
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "message": exc.detail,
                    "status": exc.status_code,
                },
            )

    def _handle_default_exception(self):
        @self.app.exception_handler(Exception)
        async def default_exception_handler(request: Request, exc: Exception):
            logger.error("Internal Server Error: %s", str(exc))
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "An unexpected error occurred",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
            )
