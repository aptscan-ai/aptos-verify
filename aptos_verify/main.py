from aptos_verify.rules.compare_bytecode import process_compare_bycode
from aptos_verify.config import get_logger
from aptos_verify.schemas import CliArgs
from aptos_verify.schemas import OutputResult
from aptos_verify.memory import __all__

logger = get_logger(__name__)

__all__ = [
    "start_verify"
]

list_rules = [
    # compare bytecode between source code that deployed onchain and bytecode onchain
    process_compare_bycode
]


async def start_verify(args: CliArgs) -> list[OutputResult]:
    """
    Start verify a module with given address (ex: 0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::swap_utils)
    """
    rs = []
    logger.info("Start process rules...")
    for rule in list_rules:
        check: OutputResult = await rule(args)
        rs.append(check)
        logger.info(f"""
                    **************** Rule: {check.title} *****************
                    Result: {check.result}
                    Error Code: {check.error_code}
                    Message: {check.message}
                    Exception Class: {check.exeption_name}
                    """)

    return rs
