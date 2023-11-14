from pydantic import BaseModel
from typing import Optional
import typing


class Params(BaseModel):

    aptos_rpc_version: typing.Optional[str] = 'v1'
    aptos_node_url: typing.Optional[str] = 'https://fullnode.mainnet.aptoslabs.com'
    compile_bytecode_version: typing.Optional[str] = ''


class CliArgs(BaseModel):
    module_id: str
    params: Optional[Params]


class OutputResult(BaseModel):
    title: str
    message: str
    is_skip: bool = False
    error_code: Optional[int] = 0
    exeption_name: Optional[str] = ""
    result: bool | None
