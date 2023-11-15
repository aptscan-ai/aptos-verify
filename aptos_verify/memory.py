
__all__ = ["LocalMemory"]


class LocalMemory():
    __store = {}

    @staticmethod
    def get(key, default=None):
        return LocalMemory.__store.get(key, default)

    @staticmethod
    def set(key, value):
        LocalMemory.__store[key] = value
