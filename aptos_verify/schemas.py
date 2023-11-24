from pydantic import BaseModel
import traceback
from typing import Optional
import typing
from pydantic import BaseModel, Field, field_validator
from aptos_verify.exceptions import ValidationError
from aptos_verify.const import VerifyMode
import os
from pathlib import Path


class VerifyArgs(BaseModel):
    module_id: str
    verify_mode: Optional[str] = VerifyMode.ONCHAIN.value
    aptos_rpc_version: typing.Optional[str] = 'v1'
    aptos_node_url: typing.Optional[str] = 'https://fullnode.mainnet.aptoslabs.com'
    compile_bytecode_version: typing.Optional[str] = ''
    move_build_path: typing.Optional[str] = os.path.join(
        str(Path.home()), 'aptos_verify_tmp')
    github_repo: typing.Optional[str] = ''
    local_path: typing.Optional[str] = ''
    keep_build_data: typing.Optional[bool] = False

    @field_validator('move_build_path')
    @classmethod
    def validate_move_build_path(cls, v: str) -> str:
        v = str(v).strip() if v else ''
        if v in ['/', '/*', '*']:
            raise ValidationError(
                "Path to to build source code is invalid. [/,/*,*] are not excepted.")
        return v

    @field_validator('keep_build_data')
    @classmethod
    def validate_clean(cls, v: str) -> str:
        return True if v == 'true' or v is True else False

    @field_validator('module_id')
    @classmethod
    def validate_module(cls, v: str) -> str:
        spl = v.split('::') if v else ''
        address, module_name = spl if len(spl) > 1 else ("", "")
        if not address or not module_name:
            raise ValidationError(
                "Module Address is invalid. Example: 0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin")
        return v

    @field_validator('verify_mode')
    @classmethod
    def validate_mode(cls, v: str) -> str:
        from aptos_verify.const import VerifyMode
        if v not in VerifyMode.values():
            raise ValidationError(
                f"Execute Mode is invalid. Allowed Mode: {VerifyMode.values()} ")
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
