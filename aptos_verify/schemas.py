from pydantic import BaseModel
import traceback
from typing import Optional
import typing
from pydantic import BaseModel, Field, field_validator
from aptos_verify.exceptions import ModuleParamIsInvalid
import os
from pathlib import Path


class Params(BaseModel):

    aptos_rpc_version: typing.Optional[str] = 'v1'
    aptos_node_url: typing.Optional[str] = 'https://fullnode.mainnet.aptoslabs.com'
    compile_bytecode_version: typing.Optional[str] = ''
    move_build_path: typing.Optional[str] = os.path.join(
        str(Path.home()), 'aptos_verify_tmp')


class CliArgs(BaseModel):
    module_id: str
    params: Optional[Params]

    @field_validator('module_id')
    @classmethod
    def validate_module(cls, v: str) -> str:
        if v == '' or not v:
            raise ModuleParamIsInvalid()
        address, module_name = v.split('::')
        if not address or not module_name:
            raise ModuleParamIsInvalid()
        return v

    @property
    def account_address(self):
        address, module_name = self.module_id.split('::')
        return address

    @property
    def module_name(self):
        address, module_name = self.module_id.split('::')
        return module_name


class OutputResult(BaseModel):
    title: str
    message: str
    is_skip: bool = False
    error_code: Optional[int] = 0
    exeption_name: Optional[str] = ""
    result: bool | None
    traceback: Optional[str] = ""
    error_message: Optional[str] = ""
