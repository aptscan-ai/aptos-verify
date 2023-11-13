from pydantic import BaseModel
import logging
import os
import argparse
from aptos_verify.memory import LocalMemory
import typing


__store_local_key = 'local_store_global_config'


class Config(BaseModel):

    aptos_rpc_version: typing.Optional[str] = 'v1'
    aptos_node_url: typing.Optional[str] = 'https://fullnode.mainnet.aptoslabs.com'
    log_level: typing.Optional[int] = logging.INFO
    compile_bytecode_version: typing.Optional[str] = ''

    @property
    def root_dir(self) -> str:
        return f'{os.path.abspath(os.curdir)}/'

    @property
    def move_template_path(self) -> str:
        return os.path.join(self.root_dir, 'move/template/')

    @property
    def move_build_path(self) -> str:
        return os.path.join(self.root_dir, 'move/current/')


def get_logger(name: str, config: Config = None):
    # Init Logger
    log_level = config.log_level if config else logging.DEBUG
    logging.basicConfig(
        level=log_level,
        format="[%(filename)s:%(lineno)s] %(asctime)s [%(levelname)s] %(message)s" if log_level < 11 else "%(asctime)s [%(levelname)s] %(message)s"
    )
    return logging.getLogger(name)


logger = get_logger(__name__)


def set_config(**kwargs) -> Config:
    logger.debug(f"Update global config with values: {kwargs}")
    _cf = LocalMemory.get(__store_local_key)
    if _cf is None:
        _cf = Config(**kwargs)
    else:
        print(kwargs)
        for k, v in kwargs.items():
            setattr(_cf, k, v)
    return LocalMemory.set(__store_local_key, _cf)


def get_config() -> Config:
    _cf = LocalMemory.get(__store_local_key)
    if not _cf:
        set_config()
    return _cf
