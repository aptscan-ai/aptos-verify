from pydantic import BaseModel
from typing import Optional


class CmdArgs(BaseModel):
    module_id: str
    node_url: Optional[str] = ""


class OutputResult(BaseModel):
    title: str
    rule_id: str
    message: str
