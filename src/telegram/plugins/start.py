from pyrogram import filters, Client

from src.telegram.enums import Message
from src.bot import bot


@bot.on_message(filters=filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    me = await client.get_me()
    await message.reply(f"Hello, I'm {me.first_name}. ")
