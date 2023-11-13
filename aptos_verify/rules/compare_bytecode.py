# This rule will check code that public onchain with current bytecode of one module_id
from aptos_verify.utils import AptosRpcUtils, AptosBytecodeUtils, AptosModuleUtils
from aptos_verify.schemas import CliArgs, Params
from aptos_verify.config import Config, get_logger, get_config
from aptos_verify.exceptions import ModuleNotFoundException
import asyncio
from aptos_verify.decorators import config_rule
import aptos_verify.exceptions as verify_exceptions

logger = get_logger(__name__)


async def get_bytecode_from_source_code_onchain(account_address: str, module_name: str, params: Params = Params()):
    """
    Get source code onchain and build by a Move Template.
    """
    # get source code onchain
    module_data = await AptosRpcUtils.rpc_account_get_source_code(account_address=account_address, module_name=module_name)
    flat_modules = [module_data.get('module')] + \
        module_data.get('related_modules')

    config = get_config()

    merge_source_code_string = ""
    for source_code in flat_modules:
        bytecode = source_code.get('source')
        if not bytecode or bytecode.replace('0x', '') == '':
            raise verify_exceptions.ModuleHasNoSourceCodeOnChainException()
        package = source_code.get('package')
        decompressed_source_code = AptosBytecodeUtils.decompress_bytecode(
            bytecode)
        manifest = AptosBytecodeUtils.decompress_bytecode(
            package.get('manifest'))
        merge_source_code_string = merge_source_code_string + \
            '\n' + decompressed_source_code

    # build bytecode from source code thats pulled onchain
    try:
        buid_res = await AptosModuleUtils.build_from_template(manifest=manifest, source_code=merge_source_code_string, 
                                                              force=True, aptos_framework_rev='',
                                                              bytecode_compile_version=params.compile_bytecode_version if params.compile_bytecode_version else '',)
    except verify_exceptions.CanNotBuildModuleException:
        logger.error(
            "Build with default manifest Move.toml fail, try to replace config [dependencies.AptosFramework] with rev=main.")
        buid_res = await AptosModuleUtils.build_from_template(manifest=manifest,
                                                              source_code=merge_source_code_string,
                                                              bytecode_compile_version=params.compile_bytecode_version if params.compile_bytecode_version else '',
                                                              force=True,
                                                              aptos_framework_rev='main')
    if buid_res:
        # get bytecode from build source
        byte_from_source = await AptosBytecodeUtils.extract_bytecode_from_build(
            config.move_build_path,
            module_name=module_name
        )
        logger.info(
            "Build and extract bytecode from source code and manifest successfuly. ")
        return byte_from_source
    return None


@config_rule(title='Compare bytecode between published bytecode and published source code onchain')
async def process_compare_bycode(args: CliArgs, **krawgs):
    """
    This code will compare bytecode from onchain and source code thats deployed and published onchain
    """
    account, module_name = args.module_id.split('::')

    task_list = [get_bytecode_from_source_code_onchain(
        account_address=account, module_name=module_name, params=args.params),
        AptosRpcUtils.rpc_account_get_bytecode(
            account_address=account, module_name=module_name, params=args.params)]
    bytecode_from_source, bytecode_info_onchain = await asyncio.gather(
        *task_list
    )

    bytecode_onchain = AptosBytecodeUtils.clean_prefix(
        bytecode_info_onchain.get('bytecode'))
    bytecode_from_source = AptosBytecodeUtils.clean_prefix(
        bytecode_from_source)

    logger.debug(f"""
                 Bytecode onchain:
                 {AptosBytecodeUtils.clean_prefix(bytecode_onchain)} 
                 \n\n
                 Bytecode thats build from source onchain:
                 {AptosBytecodeUtils.clean_prefix(bytecode_from_source)}
                 """)
    return bytecode_onchain == bytecode_from_source
