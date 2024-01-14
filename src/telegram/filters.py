from typing import TYPE_CHECKING

from pyrogram.filters import create

from src.config import settings

if TYPE_CHECKING:
    from .enums import Message


async def admin_filter(_, __, m: "Message"):
    return bool(m.from_user and m.from_user.id in settings.BOT_MANAGER_IDS)


admin = create(admin_filter)
