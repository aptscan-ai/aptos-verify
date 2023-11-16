import asyncio
from argparse import ArgumentParser
from aptos_verify.memory import LocalMemory
from aptos_verify.schemas import CliArgs, Params
import pathlib
import os


def parsing_args() -> CliArgs:
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

    parser.add_argument('-bp', '--buidpath',
                        help="Set path for storing source code and build with Aptos Cli. Default store on {USER_HOME}/aptos_verify_tmp")

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
        kwargs['aptos_node_url'] = args.rpc
    if args.loglevel:
        LocalMemory.set('global_logging_level', args.loglevel)
    if args.compileversion:
        kwargs['compile_bytecode_version'] = args.compileversion

    if args.buidpath:
        kwargs['move_build_path'] = args.buidpath
    params = Params(**kwargs)

    return CliArgs(
        module_id=args.moduleaddr,
        params=params
    )


def run():
    try:
        args = parsing_args()
    except BaseException as e:
        print(e)
        exit()
    from aptos_verify.main import start_verify
    asyncio.run(start_verify(args))
