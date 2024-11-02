from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import config


SQLALCHEMY_DATABASE_URL = config.app.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

