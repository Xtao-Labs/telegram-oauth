from pyrogram import filters

from src.bot import bot
from src.config import settings
from src.telegram.enums import Client, Message
from src.telegram.message import ACCOUNT_MSG, NO_ACCOUNT_MSG
from src.users.crud import get_user_crud


async def account(message: Message, uid: int):
    crud = get_user_crud()
    user = await crud.get_by_tg_id(uid)
    if user:
        await message.reply(ACCOUNT_MSG % (user.tg_id, user.username), quote=True)
    else:
        await message.reply(NO_ACCOUNT_MSG % uid, quote=True)


@bot.on_message(filters=filters.private & filters.command("account"))
async def get_account(_: Client, message: Message):
    uid = message.from_user.id
    if uid in settings.BOT_MANAGER_IDS and len(message.command) >= 2 and message.command[1].isnumeric():
        uid = int(message.command[1])
    await account(message, uid)
