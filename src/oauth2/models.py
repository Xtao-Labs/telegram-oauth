from typing import TYPE_CHECKING, Optional

from pydantic.types import UUID4
from sqlmodel.main import Field, Relationship

from ..storage.models import BaseTable

if TYPE_CHECKING:  # pragma: no cover
    from ..users.models import User


class Client(BaseTable, table=True):  # type: ignore
    client_id: str
    client_secret: str
    grant_types: str
    response_types: str
    redirect_uris: str

    scope: str


class AuthorizationCode(BaseTable, table=True):  # type: ignore
    code: str
    client_id: str
    redirect_uri: str
    response_type: str
    scope: str
    auth_time: int
    expires_in: int
    code_challenge: Optional[str]
    code_challenge_method: Optional[str]
    nonce: Optional[str]

    user_id: UUID4 = Field(foreign_key="users.id", nullable=False)
    user: "User" = Relationship(back_populates="user_authorization_codes")


class Token(BaseTable, table=True):  # type: ignore
    access_token: str
    refresh_token: str
    scope: str
    issued_at: int
    expires_in: int
    refresh_token_expires_in: int
    client_id: str
    token_type: str
    revoked: bool

    user_id: UUID4 = Field(foreign_key="users.id", nullable=False)
    user: "User" = Relationship(back_populates="user_tokens")
