from aptos_verify.rules.compare_bytecode import process_compare_bycode
from aptos_verify.config import get_logger
from aptos_verify.schemas import CmdArgs
from aptos_verify.schemas import OutputResult

logger = get_logger(__name__)

list_rules = [
    process_compare_bycode
]


def format_output_message(result: list):
    return result


async def process_rules(args: CmdArgs):
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

    return format_output_message(rs)
