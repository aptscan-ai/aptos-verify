from aptos_verify.main import start_verify
from aptos_verify.schemas import Args
import asyncio
from aptos_verify.config import get_config, set_config
from argparse import ArgumentParser
from aptos_verify.schemas import Args


def parsing_args() -> Args:
    """
    Parsing args from cmd
    """

    parser = ArgumentParser(
        prog='Aptos Verify Module',
        description='Libray and tools that help developers can verify module on Aptos',
    )
    parser.add_argument('-m', '--moduleaddr',
                        help="Param to get Module Address. Example: 0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::math",
                        required=True
                        )
    parser.add_argument(
        '-rpc', '--rpc', help="Param to get Aptos Node RPC URL. Default is: https://fullnode.mainnet.aptoslabs.com")
    parser.add_argument('-log', '--loglevel',
                        help="You can set level to DEBUG. Default is 20 (level INFO)")
    parser.add_argument('-cv', '--compileversion',
                        help="You can set version for bytecode compile. Example: --compile-version 6")
    args = parser.parse_args()
    kwargs = {}
    # Mapping args to setup first config
    if args.rpc:
        kwargs['aptos_rpc_version'] = args.rpc
    if args.loglevel:
        kwargs['log_level'] = args.loglevel
    if args.compileversion:
        kwargs['compile_bytecode_version'] = args.compileversion

    set_config(**kwargs)

    return Args(
        module_id=args.moduleaddr,
        config=get_config()
    )


if __name__ == '__main__':

    args = parsing_args()
    print(args)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_verify(args))
    loop.close()
