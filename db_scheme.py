import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text

load_dotenv()

user = os.environ["POSTGRESQL_USER"]
password = os.environ["POSTGRESQL_PASSWORD"]
host = os.environ["POSTGRESQL_HOST"]
port = os.environ["POSTGRESQL_PORT"]
db_name = os.environ["POSTGRESQL_NAME"]
URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'

db = create_engine(URI)


CREATE_JOBS_TABLE = text("""CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    job_title TEXT,
    job_date DATE,
    job_loc TEXT,
    city_id INTEGER,
    job_summary TEXT,
    job_salary integer[],
    job_education TEXT,
    job_url TEXT,
    company_name TEXT,
    company_type TEXT,
    search_time TIMESTAMP,
    search_position TEXT,
    source TEXT,
    search_qualified TEXT,
    FOREIGN KEY(city_id) REFERENCES cities(id)

    );""")

CREATE_CITIES_TABLE = text("""CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    city TEXT,
    lat NUMERIC,
    lng NUMERIC,
    country TEXT,
    iso2 TEXT,
    admin_name TEXT,
    capital TEXT,
    population INTEGER,
    population_proper INTEGER
    );
    """)

nl = pd.read_csv("data/nl.csv")

with db.connect() as conn:
    conn.execute(CREATE_CITIES_TABLE)
    conn.execute(CREATE_JOBS_TABLE)
    nl.to_sql(name="cities", con=conn, if_exists='append', index=False)
