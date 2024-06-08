"""Dependencies"""

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request


def valid_token_dependency(
    request: Request,
    credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
):
    """Validate the API token.

    Args:
        request (Request): The incoming request.
        credential (HTTPAuthorizationCredentials, optional): The extracted credentials. Defaults to Depends(HTTPBearer(auto_error=False)).

    Raises:
        HTTPException: Raised if the token is missing or invalid.
    """
    if request.app.state.api_key:
        if not credential or credential.credentials != request.app.state.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
