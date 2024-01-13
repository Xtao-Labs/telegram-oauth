from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .models import User
from ..storage.sqlalchemy import SQLAlchemyStorage


class SQLAlchemyCRUD:
    def __init__(self, storage: SQLAlchemyStorage):
        self.storage = storage

    async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
        q_results = await self.storage.select(
            select(User)
            .options(
                # for relationship loading, eager loading should be applied.
                selectinload(User.user_tokens)
            )
            .where(User.tg_id == tg_id)
        )

        return q_results.scalars().one_or_none()

    async def create(self, **kwargs) -> None:
        user = User(**kwargs)
        user.set_password(kwargs.get("password"))
        await self.storage.add(user)
