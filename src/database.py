from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

db_url = "slite:///./db.db"

engine = create_engine(db_url)


class Model(DeclarativeBase):
    pass


class Device(Model):
    __tablename__ = "devices"

    deviceName: Mapped[str] = mapped_column(unique=True)


Model.metadata.create_all(bind=engine)
