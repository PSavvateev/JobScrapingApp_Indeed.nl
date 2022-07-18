import os
from dotenv import load_dotenv
import requests
import psycopg2
from bs4 import BeautifulSoup


load_dotenv()

user = os.environ["POSTGRESQL_USER"]
password = os.environ["POSTGRESQL_PASSWORD"]
host = os.environ["POSTGRESQL_HOST"]
port = os.environ["POSTGRESQL_PORT"]
db_name = os.environ["POSTGRESQL_NAME"]
URI = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


class DBUpdater:
    def __init__(self):
        self.connection = psycopg2.connect(URI)

    SELECT_JOB_TO_UPDATE = """SELECT job_id, job_url FROM jobs WHERE
                   (age(current_date, job_date) >= '60 days') 
                   AND (job_status = 'active')
                   """
    UPDATE_STATUS = """UPDATE jobs
                        SET job_status = %s
                        WHERE job_id = %s
                    """

    def update_status(self):
        """
        Check and updates all the existent jobs in the database as active/inactive.

        :return: None
        """

        print('Start status updating')

        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.SELECT_JOB_TO_UPDATE)
                urls = cursor.fetchall()
                print(f'Records found: {len(urls)}')

                for url in urls:
                    print(f'job_id: {url[0]}')
                    try:
                        response = requests.get(url[1])
                        soup = BeautifulSoup(response.text, 'html.parser')
                        alert = soup.find('div', 'jobsearch-JobInfoHeader-expiredHeader').h3.text

                    except AttributeError:
                        print('Still active: pass')
                        continue

                    else:
                        cursor.execute(self.UPDATE_STATUS, ('inactive', url[0]))
                        print('Deactivated: updated')

                    finally:
                        continue
        print('End of updating session.')

    def update_city(self):
        pass

    def update_dates(self):
        pass


new_update = DBUpdater()
new_update.update_status()