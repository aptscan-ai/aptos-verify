from aptos_verify.rules.compare_bytecode import process_compare_bycode
from aptos_verify.config import get_logger
from aptos_verify.schemas import CmdArgs
import traceback

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
        check = False
        exception = 'None'

        try:
            check = await rule(args)
            rs.append(check)
        except BaseException as e:
            logger.error(f"Fail to process rule: {rule.__name__}")
            logger.debug(traceback.format_exc())
            exception = str(e)
            check = 'Skip because of exception'

        logger.info(f"""
                    **************** Rule: {rule.__name__} *****************
                    Result: {check}
                    Exception: {exception}
                    """)

    return format_output_message(rs)
