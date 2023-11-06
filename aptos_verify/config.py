from pydantic import BaseModel
import logging


class DefaultConfig(BaseModel):

    aptos_node_url: str = 'https://fullnode.mainnet.aptoslabs.com/v1'
    log_level: int = logging.DEBUG


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
