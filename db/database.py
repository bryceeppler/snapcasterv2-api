# connect to postgresql database
from sqlmodel import create_engine, SQLModel, Session
import os
# import dotenv
import dotenv
dotenv.load_dotenv()




# connect to postgresql database
pg_user = os.getenv("PG_USER")
pg_password = os.getenv('PG_PASSWORD')
pg_port = os.getenv('PG_PORT')
pg_host = os.getenv('PG_HOST')
pg_db = os.getenv('PG_DB')

pg_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

engine = create_engine(pg_url, echo=False)