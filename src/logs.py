from logging import getLogger, StreamHandler, ERROR, basicConfig, INFO, DEBUG
from coloredlogs import ColoredFormatter

logs = getLogger("telegram-oauth")
logging_format = "%(levelname)s [%(asctime)s] [%(name)s] %(message)s"
logging_handler = StreamHandler()
logging_handler.setFormatter(ColoredFormatter(logging_format))
root_logger = getLogger()
root_logger.setLevel(ERROR)
root_logger.addHandler(logging_handler)
pyro_logger = getLogger()
pyro_logger.setLevel(INFO)
pyro_logger.addHandler(logging_handler)
basicConfig(level=INFO)
logs.setLevel(INFO)
