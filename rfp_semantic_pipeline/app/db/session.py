from sqlmodel import Session, SQLModel, create_engine

from app.core.settings import get_settings


settings = get_settings()


def build_sqlite_url() -> str:
    db_path = settings.sqlite_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    # SQLite URL with absolute POSIX-style path works cross-platform, including Windows.
    return f"sqlite:///{db_path.as_posix()}"


engine = create_engine(build_sqlite_url(), echo=False)


def init_db() -> None:
    settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
