import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from src.database.models import Base

logger = logging.getLogger(__name__)

engine = create_engine(settings.COCKROACH_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        with engine.connect() as conn:
            logger.info("Ensuring pgvector extension exists...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()

        logger.info("Initializing CockroachDB tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("CockroachDB schema initialized successfully.")
    except Exception as e:
        logger.warning(f"Database setup skipped (CockroachDB not reachable): {e}")
