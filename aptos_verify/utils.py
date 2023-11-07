from aptos_verify.config import get_config
from pydantic import validate_call, Field
from aptos_sdk.async_client import RestClient
import aptos_verify.memory as local_memory
from aptos_verify.config import get_logger
import aptos_verify.exceptions as verify_exceptions
import pydantic
import typing
import zlib
from collections import namedtuple

logger = get_logger(__name__)


class AptosUtils:

    @staticmethod
    async def aptos_rest_client(**options) -> RestClient:
        """
        Init rest client instance that will be used to work with RPC API
        Docs: https://pypi.org/project/aptos-sdk/
        """
        cf = get_config()
        return RestClient(
            base_url=cf.aptos_node_url,
            **options
        )

    @staticmethod
    @pydantic.validate_call
    async def rpc_account_get_package(account_address: typing.Annotated[str, Field(min_length=5)], **option) -> list[dict]:
        """
        Get resources of an account by given account address
        """
        client = await AptosUtils.aptos_rest_client()
        logger.info(
            f'Call Aptos RPC to get resoures of account: {account_address}')
        key = f'local_cache_account_package_{account_address}'
        rs = local_memory.get(key=key)
        if local_memory.get(key=key):
            return rs
        resources = await client.account_resource(
            account_address=account_address, resource_type='0x1::code::PackageRegistry')
        if resources:
            rs = resources.get('data', {}).get('packages')
            local_memory.set(key=key, value=rs)
            return rs
        raise verify_exceptions.PackagesNotFoundException()

    @staticmethod
    @pydantic.validate_call
    async def rpc_account_get_source_code(account_address: typing.Annotated[str, Field(min_length=5)],
                                          module_name: typing.Annotated[str, Field(min_length=1)]) -> str:
        """
        Get source code of a module
        """
        packages = await AptosUtils.rpc_account_get_package(account_address=account_address)
        for package in packages:
            for module in package.get('modules', []):
                if module.get('name') == module_name:
                    return {
                        'source': module.get('source'),
                        'source_map': module.get('source_map'),
                        'module_name': module.get('name'),
                        'package': package
                    }
        raise verify_exceptions.ModuleNotFoundException()

    @staticmethod
    @pydantic.validate_call
    async def rpc_account_get_bytecode(account_address: typing.Annotated[str, Field(min_length=5)],
                                       module_name: typing.Annotated[str, Field(min_length=1)]) -> str:
        logger.info(
            f'Start get bytecode of module: {account_address}::{module_name}')
        key = f'local_cache_account_module_bytecode_{account_address}_{module_name}'
        rs = local_memory.get(key=key)
        if local_memory.get(key=key):
            return rs
        sdk_client = await AptosUtils.aptos_rest_client()
        client = sdk_client.client
        request = f"{sdk_client.base_url}/accounts/{account_address}/module/{module_name}"
        response = await client.get(request)
        if response.status_code >= 400:
            raise verify_exceptions.ApiError(f"{response.text} - {account_address}",
                                             response.status_code)

        rs = response.json()
        local_memory.set(key=key, value=rs)
        return rs


class AptosBytecodeUtils:

    @staticmethod
    @pydantic.validate_call
    def decompress_bytecode(hex_string: typing.Annotated[str, Field(min_length=5)]) -> str:
        unit8_hex_bytes = bytearray(
            bytes.fromhex(hex_string.replace('0x', '')))
        decompressed_data = zlib.decompress(unit8_hex_bytes, 15+32)
        decompressed_source_code = str(decompressed_data.decode('utf-8'))
        return decompressed_source_code

    @staticmethod
    @pydantic.validate_call
    def extract_bytecode_from_build(path: typing.Annotated[str, Field(min_length=1)]) -> str:
        """
        This method will extract bytecode from a build project move
        """
        bytecode = ''
        return bytecode
