"""Engine arguments"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AsyncEngineArgs:
    """A dataclass representing the arguments required to initialize an asynchronous engine.

    Attributes:
        model (str): The path or identifier of the model to be used by the engine.
        served_model_name (Optional[str]): An optional name to be used for serving the model.
                                            If not provided, it is derived from the last two segments of the model path.
        trust_remote_code (bool): Whether to trust remote code.
    """

    model: str
    served_model_name: Optional[str] = None
    trust_remote_code: bool = True

    def __post_init__(self):
        if self.served_model_name is None:
            self.served_model_name = "/".join(self.model.split("/")[-2:])
