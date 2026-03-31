from sqlmodel import Session, SQLModel, create_engine

from app.core.settings import get_settings


settings = get_settings()
engine = create_engine(f"sqlite:///{settings.sqlite_path}", echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
