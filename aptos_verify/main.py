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
    module_id = ''
    for rule in list_rules:
        try:
            rs.append(await rule(args))
        except BaseException as e:
            logger.error(f"Fail to process rule: {rule.__name__}")
            logger.debug(traceback.format_exc())
            pass

    return format_output_message(rs)
