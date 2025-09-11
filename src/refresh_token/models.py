from sqlmodel import SQLModel, Field
import datetime
from typing import Optional
import uuid


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True
    )
    token: str = Field(unique=True, index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    expires_at: datetime.datetime
    is_revoked: bool = Field(default=False)
    created_date: Optional[datetime.datetime] = None
    updated_date: Optional[datetime.datetime] = None
