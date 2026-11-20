from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from database import engine
from enums import *


class Model(DeclarativeBase):
    pass


class Device(Model):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)  # user readable name
    name: Mapped[str] = mapped_column()  # user readable name
    tag: Mapped[str] = mapped_column(
        unique=True
    )  # the unique id that is entered at the level of the MC
    category: Mapped[DeviceType] = mapped_column()
    department: Mapped[Department] = mapped_column()
    has_image: Mapped[bool] = mapped_column(default=False)


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
    has_profile_pic: Mapped[bool] = mapped_column(default=False)


class Event(Model):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[EventType] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    detail: Mapped[str] = mapped_column(String(255))


Model.metadata.drop_all(bind=engine)
Model.metadata.create_all(bind=engine)
