from aptos_sdk.async_client import ApiError


class PackagesNotFoundException(BaseException):
    def __init__(self, message='Cannot find any packages with given account'):
        return super().__init__(message)


class ModuleNotFoundException(BaseException):
    def __init__(self, message='Cannot find any module with given name'):
        return super().__init__(message)


class ModuleHasNoSourceCodeOnChainException(BaseException):
    def __init__(self, message='Cannot find source code onchain with given module address'):
        return super().__init__(message)


class CurrentBuildModuleInProcessException(BaseException):
    def __init__(self, message='Current path for building module move is in process.'):
        return super().__init__(message)

class CmdExceException(BaseException):
    pass
