from logging import getLogger, StreamHandler, basicConfig, INFO, CRITICAL, ERROR

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
aioauth_logger = getLogger("aioauth")
aioauth_logger.setLevel(INFO)
basicConfig(level=ERROR)
logs.setLevel(INFO)
