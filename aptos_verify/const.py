import enum

class OutputErrorCode(enum.Enum):
    PACKAGE_NOT_FOUND = (1, "Cannot find any packages with given account")
    MODULE_NOT_FOUND = (2, "Cannot find any modules with given account")
    MODULE_HAS_NO_SOURCE_CODE = (3, "Cannot find source code onchain with given module address")
    MODULE_STRING_IS_INVALID = (4, "Module Address string is invalid. Example: 0x8d2d7bcde13b2513617df3f98cdd5d0e4b9f714c6308b9204fe18ad900d92609::admin")
    