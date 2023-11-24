from aptos_verify.config import get_config
from pydantic import Field
import pydantic
from aptos_sdk.async_client import RestClient
from aptos_verify.memory import LocalMemory
from aptos_verify.config import get_logger
import aptos_verify.exceptions as verify_exceptions
import typing
import zlib
import os
import tomli
import tomli_w
from subprocess import Popen, PIPE
import json
from aptos_verify.schemas import VerifyArgs
from packaging import version

logger = get_logger(__name__)


class AptosRpcUtils:

    @staticmethod
    async def aptos_rest_client(params: VerifyArgs, **options) -> RestClient:
        """
        Init rest client instance that will be used to work with RPC API
        Docs: https://pypi.org/project/aptos-sdk/
        """
        return RestClient(
            base_url=f'{params.aptos_node_url}/{params.aptos_rpc_version}',
            **options
        )

    @staticmethod
    async def rpc_account_get_package(params: VerifyArgs, **option) -> list[dict]:
        """
        Get resources of an account by given account address
        """
        client = await AptosRpcUtils.aptos_rest_client(params)
        logger.info(
            f'Call Aptos RPC to get resoures of account: {params.account_address}')
        key = f'local_cache_account_package_{params.account_address}'
        rs = LocalMemory.get(key=key)
        if LocalMemory.get(key=key):
            return rs
        resources = await client.account_resource(
            account_address=params.account_address, resource_type='0x1::code::PackageRegistry')
        if resources:
            rs = resources.get('data', {}).get('packages')
            LocalMemory.set(key=key, value=rs)
            return rs
        raise verify_exceptions.PackagesNotFoundException()

    @staticmethod
    async def rpc_account_get_source_code(params: VerifyArgs) -> str:
        """
        Get source code of a module
        """
        packages = await AptosRpcUtils.rpc_account_get_package(params)
        needed_module = {}
        all_modules = [{
            'source': module.get('source'),
            'source_map': module.get('source_map'),
            'module_name': module.get('name'),
            'package': package
        } for package in packages for module in package.get('modules', [])]
        needed_module = [k for k in all_modules if k.get(
            'module_name') == params.module_name]
        if not needed_module or not all_modules:
            raise verify_exceptions.ModuleNotFoundException()
        return {
            'module': needed_module[0],
            'related_modules': [k for k in all_modules if k.get('module_name') != params.module_name]
        }

    @staticmethod
    async def rpc_account_get_bytecode(params: VerifyArgs) -> str:
        account_address = params.account_address
        module_name = params.module_name
        logger.info(
            f'Start get bytecode of module: {account_address}::{module_name}')
        key = f'local_cache_account_module_bytecode_{account_address}_{module_name}'
        rs = LocalMemory.get(key=key)
        if LocalMemory.get(key=key):
            return rs
        sdk_client = await AptosRpcUtils.aptos_rest_client(params=params)
        client = sdk_client.client
        request = f"{sdk_client.base_url}/accounts/{account_address}/module/{module_name}"
        response = await client.get(request)
        if response.status_code >= 400:
            raise verify_exceptions.ApiError(f"{response.text} - {account_address}",
                                             response.status_code)

        rs = response.json()
        LocalMemory.set(key=key, value=rs)
        return rs


class AptosBytecodeUtils:

    @staticmethod
    def clean_prefix(hex_str: str, prefix: str = '0x'):
        return hex_str[len(prefix):] if hex_str.startswith(prefix) else hex_str

    @staticmethod
    @pydantic.validate_call
    def decompress_bytecode(hex_string: typing.Annotated[str, Field(min_length=10)]) -> str:
        unit8_hex_bytes = bytearray(
            bytes.fromhex(hex_string.replace('0x', '')))
        decompressed_data = zlib.decompress(unit8_hex_bytes, 15+32)
        decompressed_source_code = str(decompressed_data.decode('utf-8'))
        return decompressed_source_code

    @staticmethod
    @pydantic.validate_call
    async def extract_bytecode_from_build(move_path: typing.Annotated[str, Field(min_length=1)], module_name: str = '') -> str:
        """
        This method will extract bytecode from a build project move
        """
        path = os.path.join(move_path)
        logger.info(
            f"Start extract bytecode from path: {path}. (module name: [{module_name}])")
        with open(os.path.join(path, "Move.toml"), "rb") as f:
            data = tomli.load(f)

        package = data["package"]["name"]

        package_build_dir = os.path.join(path, "build", package)
        module_directory = os.path.join(package_build_dir, "bytecode_modules")
        module_paths = os.listdir(module_directory)
        modules = []
        for module_path in module_paths:
            file_name = module_path
            module_path = os.path.join(module_directory, module_path)
            if not os.path.isfile(module_path) and not module_path.endswith(".mv"):
                continue
            if module_name != '' and file_name != f'{module_name}.mv':
                continue
            with open(module_path, "rb") as f:
                module = f.read()
                modules.append(module)
        if not modules:
            raise verify_exceptions.ModuleNotBuild()
        return bytes(modules[0]).hex()


class ExecuteCmd():

    @staticmethod
    def check_aptos_cli_version():
        logger.info("Start check APTOS CLI version...")
        stdo, stde = ExecuteCmd.exec("aptos --version")
        if not stde:
            current_v = stdo.split(" ")[1].strip()
            min_version = get_config().min_aptos_cli_ver
            if version.parse(current_v) < version.parse(get_config().min_aptos_cli_ver):
                raise verify_exceptions.AptosCliException(
                    f"Your Aptos Cli Version: {current_v.strip()} too old. Please upgrade to version: {min_version} or above")
            else:
                logger.info(f"Version: {current_v} is OK!")
        else:
            raise verify_exceptions.AptosCliException(
                f"Error when run Aptos Cli: {stde}")
        return True

    @staticmethod
    def exec(cmd: str,  **kwargs):
        logger.debug(f"Start run cmd: {cmd}")
        process = Popen(cmd,
                        shell=True, stdout=PIPE, stderr=PIPE)

        process.wait()
        std_out, std_err = process.communicate()
        error_message = std_err.decode()
        stdout_message = std_out.decode()
        logger.debug(
            f'Exec cmd: {cmd} \n Stdout:\n {stdout_message} \n Stderror: \n{error_message} \n')
        return stdout_message, error_message


class AptosModuleUtils:

    FILE_LOCK_FOLDER = 'lock.lock'

    @staticmethod
    @pydantic.validate_call
    async def clean_move_build_path(path: typing.Annotated[str, Field(min_length=3)], delete_folder=False):
        logger.info(f"Start clean move build path: {path}")
        try:
            full_path = os.path.join(
                path, "*" if delete_folder is False else "")
            if full_path.strip() in ['/', '/*', '*']:
                raise ValueError(
                    f'{full_path} is invalid. path: /,/*,* are not excepted')
            ExecuteCmd.exec(
                f'rm -r {full_path}')
        except BaseException as e:
            logger.warn(f'Cannot remove path: {path} because of {str(e)}')

    @staticmethod
    @pydantic.validate_call
    async def create_move_build_path(path: typing.Annotated[str, Field(min_length=1)]):
        logger.debug(f"Start create move build path: {path}")
        config = get_config()
        ExecuteCmd.exec(
            f'mkdir -p {path}')

    @staticmethod
    @pydantic.validate_call
    async def start_build(path: typing.Annotated[str, Field(
        min_length=1)],
        bytecode_compile_version: str = ''
    ):
        ExecuteCmd.check_aptos_cli_version()
        logger.info('Start build project')
        cmd_cv = ''
        if bytecode_compile_version:
            cmd_cv = f'--bytecode-version {bytecode_compile_version}'
        stdout_message, stderr_message = ExecuteCmd.exec(
            f'cd {path} && aptos move compile {cmd_cv}')
        stdout_message = json.loads(stdout_message)
        if not stdout_message.get('Result'):
            raise verify_exceptions.CanNotBuildModuleException(
                message=(
                    f'\nstdout: \n {stdout_message}\n{stderr_message}'))
        return stdout_message, stderr_message

    @staticmethod
    @pydantic.validate_call
    async def build_from_template(manifest: typing.Annotated[str, Field(min_length=5)],
                                  source_code: typing.Annotated[str, Field(
                                      min_length=10)],
                                  move_build_path: typing.Annotated[str, Field(
                                      min_length=1)],
                                  force: bool = True,
                                  bytecode_compile_version='',
                                  aptos_framework_rev: str = ''
                                  ):

        config = get_config()
        real_move_build_path = move_build_path
        logger.info(
            f"Start build module and save into path: {real_move_build_path}")
        await AptosModuleUtils.create_move_build_path(real_move_build_path)
        if force:
            # remove all files on move_build_path
            await AptosModuleUtils.clean_move_build_path(real_move_build_path)
        elif os.path.isfile(os.path.join(real_move_build_path, AptosModuleUtils.FILE_LOCK_FOLDER)):
            raise verify_exceptions.CurrentBuildModuleInProcessException()

        # copy all file on template to current path
        ExecuteCmd.exec(
            f'cp -rip {os.path.join(config.move_template_path,"*")} {os.path.join(real_move_build_path,"")}')

        # replace template with given params
        logger.info('Create Move.toml from manifest')
        if aptos_framework_rev != '':
            parse_toml = tomli.loads(manifest)
            dependencies = parse_toml['dependencies']
            for key, element in dependencies.items():
                if key in ['AptosFramework', 'AptosStdlib']:
                    element['rev'] = aptos_framework_rev
                    dependencies[key] = element

            parse_toml['dependencies'] = dependencies
            manifest = tomli_w.dumps(parse_toml)

        move_toml_path = os.path.join(real_move_build_path, "Move.toml")
        with open(move_toml_path, 'w') as filetowrite:
            filetowrite.write(manifest)
        logger.info('Create Move.toml done')

        logger.info('Create code.move to store source code move')
        code_path = os.path.join(
            real_move_build_path, "sources/code.move")
        with open(code_path, 'w') as filetowrite:
            filetowrite.write(source_code)
        logger.info('Create sources/code.move done')
        # start build project
        await AptosModuleUtils.start_build(
            path=real_move_build_path, bytecode_compile_version=bytecode_compile_version)
        return True

    @staticmethod
    @pydantic.validate_call
    async def pull_from_github(repo: typing.Annotated[str, Field(min_length=5)], output_path: typing.Annotated[str, Field(min_length=3)]):
        logger.info(f"Start pull source code from {repo}")
        await ExecuteCmd.exec(f"git clone {repo} {output_path}")
