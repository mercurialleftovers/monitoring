from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

db_url = "sqlite:///./db.db"

engine = create_engine(
    db_url,
    echo=True,
)


SessionLocal = sessionmaker(bind=engine)


def get_db_session() -> Generator[Session]:
    with SessionLocal() as session, session.begin():
        yield session
