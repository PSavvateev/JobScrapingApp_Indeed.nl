import os
from dotenv import load_dotenv
import requests
import psycopg2


load_dotenv()

user = os.environ["POSTGRESQL_USER"]
password = os.environ["POSTGRESQL_PASSWORD"]
host = os.environ["POSTGRESQL_HOST"]
port = os.environ["POSTGRESQL_PORT"]
db_name = os.environ["POSTGRESQL_NAME"]
URI = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


SELECT_JOBURL = """SELECT job_id, job_url FROM jobs WHERE
               (age(current_date, job_date) >= '90 days') 
               AND (job_status = 'active')
               """

SELECT_CITIES = "SELECT id, city, admin_name FROM cities"

SELECT_EMPTY_CITIES = "SELECT job_id, job_loc, city_id FROM jobs WHERE city_id is NULL"

UPDATE_STATUS = """UPDATE jobs
                    SET job_status = %s
                    WHERE job_id = %s
                """
UPDATE_CITY = """UPDATE jobs
                SET city_id = ?
                WHERE job_id = ?
                """

UPDATE_DATES = """UPDATE jobs 
                SET job_date =?
                WHERE job_id = ?
                """

connection = psycopg2.connect(URI)

def update_status():
    print('Start Updating')

    with connection as conn:
        with conn.cursor() as cursor:
            cursor.execute(SELECT_JOBURL)
            urls = cursor.fetchall()
            print(f'Records found: {len(urls)}')

            for url in urls:
                print(f'job_id: {url[0]}')
                try:
                    requests.get(url[1])
                except requests.exceptions.ConnectionError:
                    cursor.execute(UPDATE_STATUS, ('inactive', url[0]))
                    print('updated')

                else:
                    print('pass')
                    continue

                finally:
                    continue
    print('End')


update_status()


def update_city():
    pass


def update_dates():
    pass