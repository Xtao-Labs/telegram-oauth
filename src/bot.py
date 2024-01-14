import pyromod.listen
from pyrogram import Client

from .config import settings

bot = Client(
    "bot",
    bot_token=settings.BOT_TOKEN,
    api_id=settings.BOT_API_ID,
    api_hash=settings.BOT_API_HASH,
    plugins={"root": "src.telegram.plugins"},
    workdir="data",
)
