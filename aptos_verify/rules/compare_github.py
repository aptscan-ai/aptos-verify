# This rule will check code from a github repo with current bytecode of one module_id
from aptos_verify.utils import AptosRpcUtils, AptosBytecodeUtils, AptosModuleUtils
from aptos_verify.schemas import VerifyArgs
from aptos_verify.config import Config, get_logger, get_config
from aptos_verify.exceptions import ModuleNotFoundException
import asyncio
from aptos_verify.decorators import config_rule
import aptos_verify.exceptions as verify_exceptions
import time
import os
logger = get_logger(__name__)


async def extract_bytecode_from_git(args: VerifyArgs, move_build_path: str):
    # clone source code from git

    byte_from_source = ''

    await AptosModuleUtils.pull_from_github(repo=args.github_repo, output_path=move_build_path)

    # start build
    buid_res = await AptosModuleUtils.start_build(path=move_build_path,
                                                  bytecode_compile_version=args.compile_bytecode_version)

    # start extract bytecode
    if buid_res:
        # get bytecode from build source
        byte_from_source = await AptosBytecodeUtils.extract_bytecode_from_build(
            move_path=move_build_path,
            module_name=args.module_name
        )
        logger.info(
            "Build and extract bytecode from source code and manifest successfuly. ")
        # clean path
        return byte_from_source

    # remove build folder
    if not args.keep_build_data:
        await AptosModuleUtils.clean_move_build_path(move_build_path)

    return ''


@config_rule(title='Compare bytecode between a github repo and published bytecode onchain')
async def process_compare_bycode_github(args: VerifyArgs):
    # clone source code from git
    move_build_path = os.path.join(
        args.move_build_path, f'buiding_{args.account_address}_{int(round(time.time() * 1000))}')
    try:
        bytecode_from_source = await extract_bytecode_from_git(args=args, move_build_path=move_build_path)
    except BaseException as e:
        if not args.keep_build_data:
            await AptosModuleUtils.clean_move_build_path(path=move_build_path, delete_folder=True)
        raise e

    bytecode_info_onchain = await AptosRpcUtils.rpc_account_get_bytecode(params=args)

    bytecode_onchain = AptosBytecodeUtils.clean_prefix(
        bytecode_info_onchain.get('bytecode'))
    bytecode_from_source = AptosBytecodeUtils.clean_prefix(
        bytecode_from_source)

    logger.debug(f"""
                 Bytecode from github:
                 {AptosBytecodeUtils.clean_prefix(bytecode_onchain)} 
                 \n\n
                 Bytecode thats build from source onchain:
                 {AptosBytecodeUtils.clean_prefix(bytecode_from_source)}
                 """)
    if not args.keep_build_data:
        await AptosModuleUtils.clean_move_build_path(path=move_build_path, delete_folder=True)
    return bytecode_onchain == bytecode_from_source
