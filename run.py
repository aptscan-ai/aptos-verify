from aptos_verify.main import process_rules
from aptos_verify.schemas import CmdArgs
import asyncio


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    args = CmdArgs(
        module_id="afd848a070e55f593f739bdacab6c1c9b526abd39ae8b6f0dd60a53f9db2cebc::message1"
    )
    loop.run_until_complete(process_rules(args))
    loop.close()
