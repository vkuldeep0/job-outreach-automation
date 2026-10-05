import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = (
	f"postgresql+psycopg://"
	f"{os.getenv('DB_USER')}:"
	f"{os.getenv('DB_PASSWORD')}@"
	f"{os.getenv('DB_HOST')}:"
	f"{os.getenv('DB_PORT')}/"
	f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
	bind=engine,
	autoflush=False,
	autocommit=False,
)

class Base(DeclarativeBase):
	pass

