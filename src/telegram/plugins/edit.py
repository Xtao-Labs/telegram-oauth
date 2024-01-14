from pyrogram import filters

from pyromod.utils.errors import TimeoutConversationError
from src.bot import bot
from src.logs import logs
from src.telegram.enums import Client, Message
from src.telegram.filters import admin
from src.telegram.message import REG_MSG, MAIL_REGEX
from src.users.crud import get_user_crud


async def reg(client: Client, from_id: int, uid: int):
    msg_ = await client.send_message(from_id, REG_MSG)
    try:
        msg = await client.listen(from_id, filters=filters.text, timeout=60)
    except TimeoutConversationError:
        await msg_.edit("响应超时，请重试")
        return
    if msg.text and MAIL_REGEX.match(msg.text):
        crud = get_user_crud()
        try:
            user = await crud.get_by_tg_id(uid)
            if user:
                await crud.update(user, username=msg.text)
            else:
                await crud.create(
                    username=msg.text,
                    password="1",
                    tg_id=uid,
                )
        except Exception as e:
            logs.exception("注册失败", exc_info=e)
            await msg.reply_text("注册失败")
        await msg.reply_text("注册成功")
    else:
        await msg.reply_text("邮箱格式错误")


@bot.on_message(filters=filters.private & filters.command("edit") & admin)
async def edit_account(client: Client, message: Message):
    uid = from_id = message.from_user.id
    if len(message.command) >= 2 and message.command[1].isnumeric():
        uid = int(message.command[1])
    await reg(client, from_id, uid)
