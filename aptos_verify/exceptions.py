from aptos_sdk.async_client import ApiError

class PackagesNotFoundException(BaseException):
    def __init__(self, message='Cannot find any packages with given account'):
        return super().__init__(message)


class ModuleNotFoundException(BaseException):
    def __init__(self, message='Cannot find any module with given name'):
        return super().__init__(message)
