from pydantic import BaseModel
from typing import Optional, Union


class HealthCheck(BaseModel):
    payload: Optional[Union[str, int, float, dict, list]] = None
    message: Optional[str] = None
    code: Optional[int] = None


class Root(BaseModel):
    payload: Optional[Union[str, int, float, dict, list]] = None
    message: Optional[str] = None
    code: Optional[int] = None
