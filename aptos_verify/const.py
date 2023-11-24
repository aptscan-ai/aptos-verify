import enum


class OutputErrorCode(enum.Enum):
    PACKAGE_NOT_FOUND = (1, "Cannot find any packages with given account")
    MODULE_NOT_FOUND = (2, "Cannot find any modules with given account")
    MODULE_HAS_NO_SOURCE_CODE = (
        3, "Cannot find source code onchain with given module address")
    VALIDATE_PARAM_ERROR = (4, "Validation Error")


class VerifyMode(enum.Enum):
    ONCHAIN = 'onchain'
    GITHUB = 'github'
    LOCAL_PATH = 'local'

    def values():
        return [e.value for e in VerifyMode]
