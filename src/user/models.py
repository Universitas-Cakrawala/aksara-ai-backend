from sqlmodel import SQLModel, Field
import datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True
    )
    username: str = Field(unique=True, index=True)
    password: str
    is_active: bool
    deleted: bool = Field(default=False)
    created_by: str
    created_date: Optional[datetime.datetime] = None
    updated_by: str
    updated_date: Optional[datetime.datetime] = None


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profile"
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True
    )
    id_user: str = Field(foreign_key="user.id", unique=True)
    id_satker: str = Field(foreign_key="satker.id")
    nama_lengkap: str
    email: str
    tipe_akun: str
    role: str
    deleted: bool = Field(default=False)
    created_by: str
    created_date: Optional[datetime.datetime] = None
    updated_by: str
    updated_date: Optional[datetime.datetime] = None
