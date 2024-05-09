from dataclasses import dataclass, asdict
from pydantic import BaseModel
from typing import Optional


class AsyncEngineArgs(BaseModel):
    model: str = None
    served_model_name: Optional[str] = None
    batch_size: Optional[int] = 16

    # def __post_init__(self):
    #     if self.served_model_name is None:
    #         object.__setattr__(
    #             self,
    #             "served_model_name",
    #             "/".join(self.model.split("/")[-2:]),
    #         )
