"""
SQLAlchemy database engine and session factory.

The connection string is built from settings so it works both locally
(via the Cloud SQL Auth Proxy) and inside Cloud Run.
"""

from __future__ import annotations

from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


def _build_url(settings) -> str:
    # Cloud Run + Cloud SQL commonly use a Unix socket path like
    # /cloudsql/<project>:<region>:<instance>. Build that DSN accordingly.
    if settings.db_host.startswith("/cloudsql/"):
        return (
            f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
            f"@/{settings.db_name}?host={quote_plus(settings.db_host)}"
        )

    return (
        f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )


def get_engine():
    settings = get_settings()
    url = _build_url(settings)
    return create_engine(url, pool_pre_ping=True)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
