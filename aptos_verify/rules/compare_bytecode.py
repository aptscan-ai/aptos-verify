# This rule will check code that public onchain with current bytecode of one module_id
from aptos_verify.utils import aptos_rest_client, rpc_account_get_bytecode, rpc_account_get_source_code
from aptos_verify.schemas import CmdArgs
from aptos_verify.config import get_logger
import aptos_verify.memory as memory

logger = get_logger(__name__)



async def process_compare_bycode(args: CmdArgs, **krawgs):
    account, func_name = args.module_id.split('::')
    source_code = await rpc_account_get_source_code(account_address=account, func_name=func_name)
    print(source_code.get('source'))
    
    # await get_bytecode_onchain(args.module_id)
