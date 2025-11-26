import sys
import os
from pathlib import Path
import logging

# Add backend to sys.path
backend_path = Path("backend")
sys.path.append(str(backend_path.absolute()))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify_system")

def check_db():
    logger.info("Checking database configuration...")
    try:
        from app.core.config import settings
        from app.core.database import check_db_connection, engine
        from sqlalchemy import text
        
        logger.info(f"Database URL: {settings.DATABASE_URL}")
        
        if check_db_connection():
            logger.info("✅ Database connection successful!")
            
            # Check if tables exist
            with engine.connect() as connection:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
                tables = [row[0] for row in result]
                logger.info(f"Tables found: {tables}")
                
                if not tables:
                    logger.warning("⚠️  No tables found in database. You might need to run migrations or init_db.")
        else:
            logger.error("❌ Database connection failed.")
            
    except Exception as e:
        logger.error(f"❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()

def check_env():
    logger.info("Checking environment variables...")
    env_path = backend_path / ".env"
    if env_path.exists():
        logger.info("✅ .env file found.")
    else:
        logger.warning("⚠️  .env file NOT found in backend directory.")

if __name__ == "__main__":
    logger.info("Starting system verification...")
    check_env()
    check_db()
