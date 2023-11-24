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


async def extract_bytecode_from_git(args: VerifyArgs):
    buid_res = await AptosModuleUtils.start_build(path=args.local_path)
    if buid_res:
        # get bytecode from build source
        byte_from_source = await AptosBytecodeUtils.extract_bytecode_from_build(
            move_path=args.local_path,
            module_name=args.module_name
        )
        logger.info(
            "Build and extract bytecode from source code and manifest successfuly. ")
        # clean path
        return byte_from_source
    return ''


@config_rule(title='Compare bytecode between a local path and published bytecode onchain')
async def process_compare_bycode_local_path(args: VerifyArgs):
    task_list = [
        extract_bytecode_from_git(args),
        AptosRpcUtils.rpc_account_get_bytecode(params=args)
    ]

    bytecode_from_source, bytecode_info_onchain = await asyncio.gather(
        *task_list
    )

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
    return bytecode_onchain == bytecode_from_source
