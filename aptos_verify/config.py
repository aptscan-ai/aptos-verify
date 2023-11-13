import aptos_verify.config
from pydantic import BaseModel
import logging
import os
import argparse
from aptos_verify.memory import LocalMemory
import typing


__store_local_key = 'local_store_global_config'


class Config(BaseModel):
    log_level: typing.Optional[int] = logging.INFO

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


def get_config() -> Config:
    return Config()
