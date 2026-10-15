from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine
from enums import *


class Model(DeclarativeBase):
    pass


class Device(Model):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)  # user readable name
    deviceName: Mapped[str] = mapped_column()  # user readable name
    identifier: Mapped[str] = mapped_column(
        unique=True
    )  # the unique id that is entered at the level of the MC
    category: Mapped[DeviceType] = mapped_column()
    department: Mapped[Department] = mapped_column()


print("models being created ...")
# Model.metadata.drop_all(bind=engine)
Model.metadata.create_all(bind=engine)
