from pydantic import BaseModel
from typing import Optional
from aptos_verify.config import Config


class Args(BaseModel):
    module_id: str
    config: Optional[Config]


class OutputResult(BaseModel):
    title: str
    message: str
    is_skip: bool = False
    error_code: Optional[int] = 0
    exeption_name: Optional[str] = ""
    result: bool | None
