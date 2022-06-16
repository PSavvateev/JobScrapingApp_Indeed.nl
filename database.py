import sqlite3
import pandas as pd


class DBEngine:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db")


    CREATE_JOBS_TABLE = """CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        job_id TEXT,
        job_title TEXT,
        job_date TEXT,
        job_loc TEXT,
        job_city_id INTEGER,
        job_summary TEXT,
        job_salary TEXT,
        job_education TEXT,
        job_url TEXT,
        company_name TEXT,
        company_type TEXT,
        search_time TEXT,
        search_position TEXT,
        source TEXT,
        search_qualified TEXT,
        FOREIGN KEY(job_city_id) REFERENCES cities_nl(id)
                
        );"""

    CREATE_CITIES_TABLE = """CREATE TABLE IF NOT EXISTS cities_nl (
        id INTEGER PRIMARY KEY,
        city TEXT,
        lat REAL,
        lng REAL,
        country TEXT,
        iso2 TEXT,
        admin_name TEXT,
        capital TEXT,
        population INTEGER,
        population_proper INTEGER
        );
        """
    SELECT_20_JOBS = "SELECT * FROM jobs LIMIT 20"
    SELECT_CITIES = "SELECT id, city FROM cities_nl"
    SELECT_CITIES_ALL = " SELECT * from cities_nl"

    def add_cities_nl(self):
        nl = pd.read_csv("data/nl.csv")
        with self.connection:
            self.connection.execute(self.CREATE_CITIES_TABLE)
            nl.to_sql(name="cities_nl", con=self.connection, if_exists='append', index=False)

    def add_data_dump(self, df):
        with self.connection:
            self.connection.execute(self.CREATE_JOBS_TABLE)
            df.to_sql(name="jobs", con=self.connection, if_exists='append', index=False)

    def get_city_id(self):
        with self.connection:
            cities = pd.read_sql(self.SELECT_CITIES, self.connection)
            return cities

    def get_cities_all(self):
        with self.connection:
            cities = pd.read_sql(self.SELECT_CITIES_ALL, self.connection)
            return cities

    def get_jobs(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.SELECT_20_JOBS)
            return cursor.fetchall()

