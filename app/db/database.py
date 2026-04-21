from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def configure_sqlite_foreign_keys(sqlalchemy_engine) -> None:
    if sqlalchemy_engine.url.get_backend_name() != "sqlite":
        return

    @event.listens_for(sqlalchemy_engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


configure_sqlite_foreign_keys(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
