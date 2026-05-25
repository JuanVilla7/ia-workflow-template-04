from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

connect_args = {}
engine_kwargs = {"pool_pre_ping": True}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # SQLite doesn't support pool_pre_ping well in all cases and uses StaticPool by default for :memory:
    # but for file-based we can just disable it to be safe.
    engine_kwargs["pool_pre_ping"] = False

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
