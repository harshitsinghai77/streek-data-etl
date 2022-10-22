import os

import databases
import sqlalchemy

DB_NAME = os.getenv("DB_NAME", "streek")
DB_USER = os.getenv("DB_USER", "streek")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_MAX_SIZE = 10

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = databases.Database(DATABASE_URL + f"?min_size=1&max_size={DB_MAX_SIZE}")
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
