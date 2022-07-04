import os
import pandas as pd
from dotenv import load_dotenv
import requests
import time

SELECT_JOBID = "SELECT job_id, job_url FROM jobs WHERE (age(current_date, job_date) >= '30 days' )"

SELECT_CITIES = "SELECT id, city, admin_name FROM cities"

SELECT_EMPTY_CITIES = "SELECT job_id, job_loc, city_id FROM jobs WHERE city_id is NULL"

UPDATE_STATUS = """UPDATE jobs_statuses 
                    SET job_id = "inactive" 
                    WHERE job_id = ?
                """
UPDATE_CITY = """UPDATE jobs
                SET city_id = ?
                WHERE job_id = ?
                """

UPDATE_DATES = """UPDATE jobs 
                SET job_date =?
                WHERE job_id = ?
                """

urls = []

def update_status():
    for url in urls:

        try:
            response = requests.get(url)
        except AttributeError:
            # update the status in the  job_status for "inactive"
            pass
        else:
            continue

        finally:
            continue


def update_city():
    pass


def update_dates():
    pass