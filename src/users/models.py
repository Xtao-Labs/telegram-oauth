from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from sqlalchemy import Column, BigInteger
from sqlmodel.main import Field, Relationship

from ..storage.models import BaseTable

if TYPE_CHECKING:  # pragma: no cover
    from ..oauth2.models import AuthorizationCode, Token


class UserAnonymous(BaseModel):
    @property
    def is_authenticated(self) -> bool:
        return False


class User(BaseTable, table=True):  # type: ignore
    __tablename__ = "users"

    is_superuser: bool = False
    is_blocked: bool = False
    is_active: bool = False

    username: str = Field(nullable=False, sa_column_kwargs={"unique": True}, index=True)
    password: Optional[str] = None
    tg_id: int = Field(sa_column=Column(BigInteger(), nullable=False))

    user_authorization_codes: List["AuthorizationCode"] = Relationship(
        back_populates="user"
    )
    user_tokens: List["Token"] = Relationship(back_populates="user")

    @property
    def is_authenticated(self) -> bool:
        return True
