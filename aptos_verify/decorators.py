import aptos_verify.memory
from aptos_verify.schemas import CliArgs, OutputResult
import traceback
from aptos_verify.config import get_logger
import traceback
logger = get_logger(__name__)


def config_rule(title: str,
                ) -> OutputResult:
    def inner_handle(func):
        async def wrapper(args: CliArgs):
            try:
                if type(args) is not CliArgs or not hasattr(args, 'module_id'):
                    raise ValueError(
                        'Args for this rule is invalid. You need to set a param that is instance of CliArgs')
                result = await func(args)
                return OutputResult(
                    title=title,
                    message="Verify success" if result else "Verify fail",
                    result=result
                )
            except BaseException as e:
                logger.debug(traceback.format_exc())
                is_skip = hasattr(e, 'verify_skip') and e.verify_skip
                error_code = e.error_code if hasattr(
                    e, 'error_code') and e.error_code else (0, "")

                return OutputResult(
                    title=title,
                    is_skip=is_skip,
                    message=f"{ 'Skip this rule' if is_skip else ''}. {error_code[1]}",
                    error_code=error_code[0],
                    exeption_name=type(e).__name__,
                    error_message=str(e),
                    traceback=traceback.format_exc() if logger.level < 20 else "",
                    result=None if is_skip else False
                )

        return wrapper
    return inner_handle
