# This rule will check code that public onchain with current bytecode of one module_id
from aptos_verify.utils import AptosRpcUtils, AptosBytecodeUtils, AptosModuleUtils
from aptos_verify.schemas import CmdArgs
from aptos_verify.config import get_logger, get_config
import aptos_verify.exceptions as verify_exceptions
import asyncio

logger = get_logger(__name__)
config = get_config()


async def get_bytecode_from_source_code_onchain(account_address: str, module_name: str):
    """
    Get source code onchain and build by a Move Template.
    """
    # get source code onchain
    source_code = await AptosRpcUtils.rpc_account_get_source_code(account_address=account_address, module_name=module_name)
    bytecode = source_code.get('source')
    if not bytecode:
        raise verify_exceptions.ModuleHasNoSourceCodeOnChainException()
    package = source_code.get('package')
    decompressed_source_code = AptosBytecodeUtils.decompress_bytecode(
        bytecode)
    manifest = AptosBytecodeUtils.decompress_bytecode(
        package.get('manifest'))
    package_name = package.get('name')
    manifest = AptosBytecodeUtils.decompress_bytecode(package.get('manifest'))

    # build bytecode from source code thats pulled onchain
    await AptosModuleUtils.build_from_template(
        account_address=account_address, manifest=manifest, source_code=decompressed_source_code, force=True)
    return
    # get bytecode from build source
    byte_from_source = await AptosBytecodeUtils.extract_bytecode_from_build(
        config.move_template_path)

    return byte_from_source
    return {
        'source_code': decompressed_source_code,
        'manifest': manifest,
        'package_name':  package_name
    }


async def process_compare_bycode(args: CmdArgs, **krawgs):
    """
    This code will compare bytecode from onchain and source code thats deployed and published onchain
    """
    
    account, module_name = args.module_id.split('::')
    return await get_bytecode_from_source_code_onchain(
            account_address=account, module_name=module_name)
    bytecode_from_source, bytecode_info_onchain = await asyncio.gather(
        get_bytecode_from_source_code_onchain(
            account_address=account, module_name=module_name),
        AptosRpcUtils.rpc_account_get_bytecode(
            account_address=account, module_name=module_name)
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
