"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.app.common.config.config import settings
import importlib.util
import logging

logger = logging.getLogger(__name__)


# Determine a DBAPI-aware SQLAlchemy URL at runtime without changing
# package files. If the settings.database_url is a plain
# 'postgresql://' URL, try to detect an installed DBAPI and add the
# appropriate '+<driver>' marker so SQLAlchemy uses the installed
# driver (psycopg v3 or psycopg2). If neither is present, fall back
# to the provided URL and let create_engine raise a helpful error.
def _resolve_sqlalchemy_url(raw_url: str) -> str:
    if not raw_url:
        return raw_url

    # Only modify postgres urls that don't already specify a driver
    if raw_url.startswith("postgresql+"):
        return raw_url

    if raw_url.startswith("postgresql://"):
        # Prefer psycopg (v3) if installed, otherwise psycopg2.
        if importlib.util.find_spec("psycopg"):
            return raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
        if importlib.util.find_spec("psycopg2"):
            return raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    return raw_url


resolved_url = _resolve_sqlalchemy_url(settings.database_url)

try:
    engine = create_engine(
        resolved_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=False,
    )
except Exception as exc:
    # Provide a clearer message including the resolved URL for easier debugging
    logger.exception("Failed to create SQLAlchemy engine for URL: %s", resolved_url)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
