"""
Setups connection and communicates with postgresql database

"""
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


class DBEngine:
    def __init__(self):
        self.db = create_engine(URI)

    SELECT_CITIES_ID = text("SELECT id, city FROM cities")

    SELECT_JOBS_ID = text("SELECT job_id FROM jobs")

    def insert_jobs(self, df):
        """
        Insert jobs into the jobs table
        :param df: pandas.DataFrame
        :return:
        """
        with self.db.connect() as conn:
            df.to_sql(name="jobs", con=conn, if_exists='append', index=False)

    def get_city_id(self):
        with self.db.connect() as conn:
            cities = pd.read_sql(self.SELECT_CITIES_ID, conn)
            return cities

    def get_job_id(self):
        with self.db.connect() as conn:
            job_ids = pd.read_sql(self.SELECT_JOBS_ID, conn)
            return job_ids
