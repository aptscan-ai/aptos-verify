from aptos_verify.config import get_config
from pydantic import Field
import pydantic
from aptos_sdk.async_client import RestClient
import aptos_verify.memory as local_memory
from aptos_verify.config import get_logger
import aptos_verify.exceptions as verify_exceptions
import typing
import zlib
import os
import tomli
from subprocess import Popen, PIPE

logger = get_logger(__name__)
config = get_config()


class AptosRpcUtils:

    @staticmethod
    async def aptos_rest_client(**options) -> RestClient:
        """
        Init rest client instance that will be used to work with RPC API
        Docs: https://pypi.org/project/aptos-sdk/
        """
        return RestClient(
            base_url=f'{config.aptos_node_url}/{config.aptos_rpc_version}',
            **options
        )

    @staticmethod
    @pydantic.validate_call
    async def rpc_account_get_package(account_address: typing.Annotated[str, Field(min_length=1)], **option) -> list[dict]:
        """
        Get resources of an account by given account address
        """
        client = await AptosRpcUtils.aptos_rest_client()
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
    async def rpc_account_get_source_code(account_address: typing.Annotated[str, Field(min_length=1)],
                                          module_name: typing.Annotated[str, Field(min_length=1)]) -> str:
        """
        Get source code of a module
        """
        packages = await AptosRpcUtils.rpc_account_get_package(account_address=account_address)
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
    async def rpc_account_get_bytecode(account_address: typing.Annotated[str, Field(min_length=1)],
                                       module_name: typing.Annotated[str, Field(min_length=1)]) -> str:
        logger.info(
            f'Start get bytecode of module: {account_address}::{module_name}')
        key = f'local_cache_account_module_bytecode_{account_address}_{module_name}'
        rs = local_memory.get(key=key)
        if local_memory.get(key=key):
            return rs
        sdk_client = await AptosRpcUtils.aptos_rest_client()
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
    def clean_prefix(hex_str: str, prefix: str = '0x'):
        return hex_str[len(prefix):] if hex_str.startswith(prefix) else hex_str

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
        with open(os.path.join(path, "Move.toml"), "rb") as f:
            data = tomli.load(f)

        package = data["package"]["name"]

        package_build_dir = os.path.join(path, "build", package)
        module_directory = os.path.join(package_build_dir, "bytecode_modules")
        module_paths = os.listdir(module_directory)
        modules = []
        for module_path in module_paths:
            module_path = os.path.join(module_directory, module_path)
            if not os.path.isfile(module_path) and not module_path.endswith(".mv"):
                continue
            with open(module_path, "rb") as f:
                print(module_path)
                module = f.read()
                modules.append(module)
        return bytes(modules[0]).hex()


class ExecuteCmd():

    @staticmethod
    def exec(cmd: str, **kwargs):
        logger.debug(f"Start run cmd: {cmd}")
        process = Popen(cmd,
                        shell=True, stdout=PIPE, stderr=PIPE)
        process.wait()
        std_out, std_err = process.communicate()
        if std_err.decode() != '':
            logger.exception(std_err.decode())
        return std_out.decode()


class AptosModuleUtils:

    FILE_LOCK_FOLDER = 'lock.lock'

    @staticmethod
    @staticmethod
    @pydantic.validate_call
    async def build_from_template(account_address: typing.Annotated[str, Field(min_length=1)],
                                  manifest: typing.Annotated[str, Field(min_length=10)],
                                  source_code: typing.Annotated[str, Field(
                                      min_length=10)],
                                  force: bool = False
                                  ):

        if force:
            # remove all files on move_build_path
            ExecuteCmd.exec(
                f'rm -r {os.path.join(config.move_build_path,"*")}')
        elif os.path.isfile(os.path.join(config.move_build_path, AptosModuleUtils.FILE_LOCK_FOLDER)):
            raise verify_exceptions.CurrentBuildModuleInProcessException()

        # copy all file on template to current path
        ExecuteCmd.exec(
            f'cp -r {os.path.join(config.move_template_path,"*")} {os.path.join(config.move_build_path,"")}')

        # replace template with given params
        logger.debug('Create Move.toml from manifest')
        move_toml_path = os.path.join(config.move_template_path, "Move.toml")
        with open(move_toml_path, 'w') as filetowrite:
            filetowrite.write(manifest)
        logger.debug('Create file that contain from manifest')
        # start build project
