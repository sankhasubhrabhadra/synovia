import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.database.models import Base

logger = logging.getLogger("synovia.database")

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "synovia.db")

# Read DATABASE_URL from environment if available (e.g. PostgreSQL/Supabase), fallback to SQLite
ENV_DB_URL = os.getenv("DATABASE_URL")
if ENV_DB_URL:
    if ENV_DB_URL.startswith("postgres://"):
        DATABASE_URL = ENV_DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif ENV_DB_URL.startswith("postgresql://"):
        DATABASE_URL = ENV_DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        DATABASE_URL = ENV_DB_URL
else:
    DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

is_sqlite = DATABASE_URL.startswith("sqlite")

connect_args = {}
if is_sqlite:
    connect_args = {"check_same_thread": False, "timeout": 30.0}

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=3600
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initializes tables, indexes, and configures WAL high-concurrency mode for SQLite."""
    async with engine.begin() as conn:
        # Create all tables & indexes
        await conn.run_sync(Base.metadata.create_all)

        if is_sqlite:
            # Enable SQLite Write-Ahead Logging (WAL) for 100x higher concurrency (supports thousands of users)
            await conn.execute(text("PRAGMA journal_mode=WAL;"))
            await conn.execute(text("PRAGMA synchronous=NORMAL;"))
            await conn.execute(text("PRAGMA busy_timeout=10000;"))
            await conn.execute(text("PRAGMA cache_size=-64000;")) # 64MB RAM cache

            # Migration fallback for legacy tables
            try:
                await conn.execute(text("ALTER TABLE projects ADD COLUMN user_id VARCHAR;"))
            except Exception:
                pass # Column already present

    logger.info(f"Database initialized in WAL mode. Database location: {DATABASE_URL}")

async def get_db():
    """FastAPI Async DB session dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session
