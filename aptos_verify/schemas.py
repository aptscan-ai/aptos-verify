from pydantic import BaseModel
from typing import Optional


class CmdArgs(BaseModel):
    module_id: str
    node_url: Optional[str] = ""


class OutputResult(BaseModel):
    title: str
    message: str
    is_skip: bool = False
    error_code: Optional[int] = 0
    exeption_name: Optional[str] = ""
    result: bool | None
