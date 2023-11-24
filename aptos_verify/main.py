from aptos_verify.rules.compare_bytecode import process_compare_bycode
from aptos_verify.rules.compare_github import process_compare_bycode_github
from aptos_verify.rules.compare_local import process_compare_bycode_local_path
from aptos_verify.config import get_logger
from aptos_verify.schemas import VerifyArgs
from aptos_verify.schemas import OutputResult
from aptos_verify.const import VerifyMode
from aptos_verify.memory import __all__

logger = get_logger(__name__)

__all__ = [
    "start_verify"
]


config_rules = {
    VerifyMode.ONCHAIN.value: process_compare_bycode,
    VerifyMode.GITHUB.value: process_compare_bycode_github,
    VerifyMode.LOCAL_PATH.value: process_compare_bycode_local_path
}


async def start_verify(args: VerifyArgs) -> list[OutputResult]:
    """
    Start verify a module with given address (ex: 0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::swap_utils)
    """
    rule = config_rules.get(args.verify_mode)
    logger.info(f"Start process verify with mode: {args.verify_mode}")
    check: OutputResult = await rule(args)
    logger.info(f"""
                    **************** Rule: {check.title} *****************
                    Result: {check.result}
                    Error Code: {check.error_code}
                    Message: {check.message}
                    Exception Class: {check.exeption_name}
                    Execption Message: {check.error_message}
                    """)
    return check
