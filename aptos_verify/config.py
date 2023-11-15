import aptos_verify.config
from pydantic import BaseModel
import logging
import os
from aptos_verify.memory import LocalMemory
import typing
try:
    log_level = LocalMemory.get('global_logging_level', logging.INFO)
    log_level = int(log_level) if log_level else 0
    if log_level not in [
        logging.CRITICAL,
        logging.FATAL,
        logging.ERROR,
        logging.WARNING,
        logging.WARN,
        logging.INFO,
        logging.DEBUG,
        logging.NOTSET
    ]:
        print(f'ERROR: log level is invalid. set default to {logging.INFO}')
        log_level = logging.INFO
except:
    log_level = logging.INFO

logging.basicConfig(
    level=log_level,
    format="[%(filename)s:%(lineno)s] %(asctime)s [%(levelname)s] %(message)s" if log_level < 11 else "%(asctime)s [%(levelname)s] %(message)s"
)


class Config(BaseModel):
    log_level: typing.Optional[int] = logging.INFO

    @property
    def root_dir(self) -> str:
        return f'{os.path.dirname(os.path.realpath(__file__))}/../'

    @property
    def move_template_path(self) -> str:
        return os.path.join(self.root_dir, 'move/template/')



def get_logger(name: str):
    return logging.getLogger(name)


logger = get_logger(__name__)


def get_config() -> Config:
    return Config()
