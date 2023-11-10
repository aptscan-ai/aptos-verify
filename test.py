

from aptos_verify.main import process_rules
from aptos_verify.schemas import CmdArgs
import asyncio
from aptos_verify.utils import AptosModuleUtils, AptosRpcUtils
import tomli


async def test(args: CmdArgs):
    from aptos_verify.utils import AptosModuleUtils, AptosBytecodeUtils
    from aptos_verify.config import get_config
    config = get_config()
    account, module_name = args.module_id.split('::')
    # bytecode = await AptosBytecodeUtils.extract_bytecode_from_build(config.move_build_path)
    # a = (await AptosRpcUtils.rpc_account_get_source_code(account_address=account, module_name=module_name))
    # print(a['module'])
    from aptos_verify.rules.compare_bytecode import get_bytecode_from_source_code_onchain
    await get_bytecode_from_source_code_onchain(account_address=account, module_name=module_name)

    
    # print(bytecode)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    args = CmdArgs(
        module_id="0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::router"
    )
    loop.run_until_complete(test(args))
    loop.close()
