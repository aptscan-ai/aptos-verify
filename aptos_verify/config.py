from pydantic import BaseModel
import logging
import os


class DefaultConfig(BaseModel):

    aptos_rpc_version: str = 'v1'
    aptos_node_url: str = 'https://fullnode.mainnet.aptoslabs.com'
    log_level: int = logging.INFO

    @property
    def root_dir(self) -> str:
        return f'{os.path.abspath(os.curdir)}/'

    @property
    def move_template_path(self) -> str:
        return os.path.join(self.root_dir, 'move/template/')

    @property
    def move_build_path(self) -> str:
        return os.path.join(self.root_dir, 'move/current/')


def parsing_from_cmdargs():
    pass


def get_config() -> DefaultConfig:
    return DefaultConfig()


def get_logger(name: str):
    # Init Logger
    logging.basicConfig(
        level=get_config().log_level,
        format="[%(filename)s:%(lineno)s] %(asctime)s [%(levelname)s] %(message)s" if get_config(
        ).log_level < 11 else "%(asctime)s [%(levelname)s] %(message)s"
    )
    return logging.getLogger(name)
