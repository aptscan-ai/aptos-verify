import asyncio
from argparse import ArgumentParser
from aptos_verify.memory import LocalMemory
from aptos_verify.schemas import VerifyArgs
from aptos_verify.const import VerifyMode
import pathlib
import os
import sys


def parsing_args() -> VerifyArgs:
    """
    Parsing args from cmd
    """
    from aptos_verify.const import VerifyMode
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

    parser.add_argument('-rpc', '--rpc',
                        help="Param to get Aptos Node RPC URL. Default is: https://fullnode.mainnet.aptoslabs.com")

    parser.add_argument('-log', '--loglevel',
                        help="You can set level to DEBUG. Default is 20 (level INFO)")
    parser.add_argument('-cv', '--compileversion',
                        help="You can set version for bytecode compile. Example: --compile-version 6")

    parser.add_argument('-vm', '--verifymode',
                        help=f"Verify module mode. Default: {VerifyMode.ONCHAIN.value}",
                        choices=set(VerifyMode.values()),
                        default=VerifyMode.ONCHAIN.value)

    parser.add_argument('-keep', '--keepbuild',
                        help=f"Keep build path folder after verify. Default this path will be removed after verify with mode ([{VerifyMode.GITHUB.value}, {VerifyMode.ONCHAIN.value}])")

    parser.add_argument('-git', '--github',
                        help="Github Repo to get source code and compare.", required=VerifyMode.GITHUB.value in sys.argv)

    parser.add_argument('-path', '--path',
                        help="Local path that store source code to build.", required=VerifyMode.LOCAL_PATH.value in sys.argv)

    args = parser.parse_args()

    kwargs = {
        'module_id': args.moduleaddr,
        'verify_mode': args.verifymode
    }

    # Mapping args to setup first config
    if args.rpc:
        kwargs['aptos_node_url'] = args.rpc
    if args.loglevel:
        LocalMemory.set('global_logging_level', args.loglevel)
    if args.compileversion:
        kwargs['compile_bytecode_version'] = args.compileversion

    if args.keepbuild:
        kwargs['keep_build_data'] = args.keepbuild

    if args.buidpath:
        kwargs['move_build_path'] = args.buidpath

    if args.github:
        kwargs['github_repo'] = args.github

    if args.path:
        kwargs['local_path'] = args.path

    return VerifyArgs(**kwargs)


def run():
    try:
        args = parsing_args()
    except BaseException as e:
        print(e)
        exit()
    from aptos_verify.main import start_verify
    asyncio.run(start_verify(args))


if __name__ == '__main__':
    print(run())
