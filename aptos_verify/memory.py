
__store = {}

__all__ = ["set", "get"]


def get(key, default=None):
    return __store.get(key, default)


def set(key, value):
    __store[key] = value
