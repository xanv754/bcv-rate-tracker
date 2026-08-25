from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from storage.models import Base
from utils.env import DatabaseConfig


class Database:
    """Singleton owning the SQLAlchemy engine and session factory for the storage layer."""

    _instance: "Database | None" = None
    _engine: Engine
    _session_factory: sessionmaker[Session]

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._engine = create_engine(DatabaseConfig.url())
            cls._instance._session_factory = sessionmaker(bind=cls._instance._engine)
        return cls._instance

    def create_tables(self) -> None:
        """Create the exchange_rates and scrape_runs tables if they do not yet exist."""
        Base.metadata.create_all(self._engine)

    def get_session(self) -> Session:
        """Open a new ORM session bound to the configured database engine."""
        return self._session_factory()
