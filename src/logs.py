from logging import getLogger, StreamHandler, basicConfig, INFO, CRITICAL

from coloredlogs import ColoredFormatter

logs = getLogger("telegram-oauth")
logging_format = "%(levelname)s [%(asctime)s] [%(name)s] %(message)s"
logging_handler = StreamHandler()
logging_handler.setFormatter(ColoredFormatter(logging_format))
root_logger = getLogger()
root_logger.setLevel(CRITICAL)
root_logger.addHandler(logging_handler)
pyro_logger = getLogger("pyrogram")
pyro_logger.setLevel(INFO)
sql_logger = getLogger("sqlalchemy")
sql_logger.setLevel(CRITICAL)
sql_engine_logger = getLogger("sqlalchemy.engine.Engine")
sql_engine_logger.setLevel(CRITICAL)
basicConfig(level=CRITICAL)
logs.setLevel(INFO)
