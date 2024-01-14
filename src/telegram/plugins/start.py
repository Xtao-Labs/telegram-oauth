from httpx import URL
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot import bot
from src.config import settings
from src.telegram.enums import Message
from src.telegram.message import NO_ACCOUNT_MSG, LOGIN_MSG, LOGIN_BUTTON
from src.users.crud import get_user_crud
from src.utils.telegram import encode_telegram_auth_data


async def login(message: Message):
    uid = message.from_user.id
    crud = get_user_crud()
    user = await crud.get_by_tg_id(uid)
    if not user:
        await message.reply(NO_ACCOUNT_MSG % uid, quote=True)
        return
    token = await encode_telegram_auth_data(uid)
    url = settings.PROJECT_URL + "/api/users/auth"
    url = URL(url).copy_add_param("jwt", token)
    url = str(url)
    await message.reply(
        LOGIN_MSG,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(LOGIN_BUTTON, url=url)]]
        ),
    )


@bot.on_message(filters=filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    if message.command and len(message.command) >= 2:
        action = message.command[1]
        if action == "login":
            await login(message)
        return
    me = await client.get_me()
    await message.reply(f"Hello, I'm {me.first_name}. ")
