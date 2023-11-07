# This rule will check code that public onchain with current bytecode of one module_id
from aptos_verify.utils import AptosUtils, AptosBytecodeUtils
from aptos_verify.schemas import CmdArgs
from aptos_verify.config import get_logger
import asyncio

logger = get_logger(__name__)


async def process_compare_bycode(args: CmdArgs, **krawgs):
    """
    This code will compare bytecode from onchain and source code thats deployed and published onchain
    """
    account, module_name = args.module_id.split('::')

    async def get_source_code_onchain():
        source_code = await AptosUtils.rpc_account_get_source_code(account_address=account, module_name=module_name)
        bytecode = source_code.get('source')
        package = source_code.get('package')
        decompressed_source_code = AptosBytecodeUtils.decompress_bytecode(
            bytecode)
        manifest = AptosBytecodeUtils.decompress_bytecode(
            package.get('manifest'))
        package_name = package.get('name')
        return {
            'source_code': decompressed_source_code,
            'manifest': manifest,
            'package_name':  package_name
        }

    async def get_bytecode_onchain():
        bytecode = await AptosUtils.rpc_account_get_bytecode(account_address=account, module_name=module_name)
        return bytecode

    source_code_info, bytecode = await asyncio.gather(
        get_source_code_onchain(),
        get_bytecode_onchain()
    )

    print(source_code_info, bytecode)

    logger.info("Compare bytecode done.")
