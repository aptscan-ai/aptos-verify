from aptos_sdk.async_client import ApiError
from aptos_verify.const import OutputErrorCode


class VerifyExceptionBase(BaseException):

    error_code = (0, "")  # a list or tupple that define code interge or
    verify_skip = False

    def __init__(self, message=""):
        return super().__init__(f'{self.error_code[1]}. {message}')


class ValidationError(VerifyExceptionBase):
    error_code = OutputErrorCode.VALIDATE_PARAM_ERROR.value


class PackagesNotFoundException(VerifyExceptionBase):
    error_code = OutputErrorCode.PACKAGE_NOT_FOUND.value


class ModuleNotFoundException(VerifyExceptionBase):
    error_code = OutputErrorCode.MODULE_NOT_FOUND.value


class ModuleHasNoSourceCodeOnChainException(VerifyExceptionBase):
    error_code = OutputErrorCode.MODULE_HAS_NO_SOURCE_CODE.value


class CurrentBuildModuleInProcessException(VerifyExceptionBase):
    verify_skip = True


class CmdExcException(VerifyExceptionBase):
    verify_skip = True


class CanNotBuildModuleException(VerifyExceptionBase):
    verify_skip = True


class ModuleNotBuild(VerifyExceptionBase):
    verify_skip = True
