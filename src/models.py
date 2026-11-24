from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from database import engine
from enums import *
from constants import DIRS


class Model(DeclarativeBase):
    pass


class Device(Model):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    tag: Mapped[str] = mapped_column(unique=True)
    category: Mapped[DeviceType] = mapped_column()
    department: Mapped[Department] = mapped_column()
    device_image: Mapped[str | None] = mapped_column(default=None)


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    role: Mapped[Role] = mapped_column()
    profile_picture: Mapped[str | None] = mapped_column(default=None)

    # @property
    # def image_path(self) -> str:
    #     if self.profile_picture:
    #         return f"{DIRS.user_profile_pictures}/{self.profile_picture}"
    #
    #     return f"{DIRS.default_pictures}/user.svg"


class Event(Model):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[EventType] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    detail: Mapped[str] = mapped_column(String(255))


Model.metadata.drop_all(bind=engine)
Model.metadata.create_all(bind=engine)
