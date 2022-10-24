# connect to postgresql database
from sqlmodel import create_engine, SQLModel
import os

# connect to postgresql database
pg_user = os.environ.get('PG_USER')
pg_password = os.environ.get('PG_PASSWORD')
pg_port = os.environ.get('PG_PORT')
pg_host = os.environ.get('PG_HOST')
pg_db = os.environ.get('PG_DB')

pg_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

engine = create_engine(pg_url, echo=True)

# create a table with the engine if they don't exist
# we need to put some of this in the api i think
SQLModel.metadata.create_all(engine)