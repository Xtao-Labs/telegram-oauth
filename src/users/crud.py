from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Update

from .models import User
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage


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
        await self.storage.add(user)

    async def update(self, user: User, **kwargs) -> None:
        await self.storage.update(
            Update(User).where(User.id == user.id).values(**kwargs)
        )


def get_user_crud(storage: SQLAlchemyStorage = None) -> SQLAlchemyCRUD:
    if storage is None:
        storage = get_sqlalchemy_storage()
    return SQLAlchemyCRUD(storage=storage)
