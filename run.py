from aptos_verify.main import process_rules
from aptos_verify.schemas import CmdArgs
import asyncio


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    args = CmdArgs(
        module_id="0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::mint"
    )
    loop.run_until_complete(process_rules(args))
    loop.close()
