"""Engine arguments"""

from typing import Optional

from pydantic import BaseModel


class AsyncEngineArgs(BaseModel):
    """A class representing the arguments required to initialize an asynchronous engine.

    Args:
        model (str): The path or identifier of the model to be used by the engine.
        served_model_name (Optional[str]): An optional name to be used for serving the model.
                                            If not provided, it is derived from the last two segments of the model path.
        trust_remote_code (Optional[bool]): Trust remote code.
    """

    model: str
    served_model_name: Optional[str] = None
    trust_remote_code: bool = True

    def __init__(self, **data):
        super().__init__(**data)
        if self.served_model_name is None:
            self.served_model_name = "/".join(self.model.split("/")[-2:])
