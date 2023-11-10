from aptos_verify.main import process_rules
from aptos_verify.schemas import CmdArgs
import asyncio


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    args = CmdArgs(
        module_id="0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::swap_utils"
    )
    loop.run_until_complete(process_rules(args))
    loop.close()
