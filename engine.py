import time
from indeed_nl_scraper import get_jobs
from database import DBEngine
from dumping import DataDump
from logger import Logger


class ScrapingSession:
    def __init__(self, positions, company_types, education_level, red_flags):
        self.positions = positions
        self.company_types = company_types
        self.education_level = education_level
        self.red_flags = red_flags

    def run(self):
        data_dump = DataDump()
        logger = Logger()
        database = DBEngine()

        database.add_cities_nl()

        # scraping -> creates a compiled data dump from different search parameters
        logger.start_session()  # logging start of a session

        for position in self.positions:

            for company_type in self.company_types:

                logger.start_scraping(position, company_type, self.education_level)  # logging each scraping attempt

                try:
                    df = get_jobs(position, company_type, self.education_level)
                except Exception as inst:
                    logger.error_occurs(inst)
                else:
                    logger.scraping_result(df)  # logging scraping results
                    data_dump.merge(df)  # merging all values to the data_dump
                finally:
                    time.sleep(5)  # wait for 5 seconds to avoid a block
                    continue

        logger.scraping_result_final(data_dump.df)  # logging scraping results

        # data cleansing / formatting
        data_dump.remove_duplicates(field="job_id")  # removing duplicates
        # data_dump.date_fields_format(fields=["job_date", "search_time"]) -> not needed at this version
        data_dump.add_qualification(red_flags=self.red_flags)  # adding qualification column with True / False
        data_dump.add_job_city_id(field="job_loc", db=database.get_city_id())  # adding city id from related SQL table

        data_dump.format_salaries(field="job_salary")

        logger.data_formatted(data_dump.df)  # logging formatted data dump information

        # saving as a csv file
        data_dump.save_to_csv(path="data_dumps/")

        # saving to SQLite DataBase
        database.add_data_dump(data_dump.df)

        logger.end_session()
        logger.save_to_txt()
