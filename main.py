import time
import indeed_nl_scraper
from database import DBEngine
from dumping import DataDump
from logger import Logger


class ScrapingSession:
    def __init__(self, positions, company_types, education_levels, red_flags):
        self.positions = positions
        self.company_types = company_types
        self.education_levels = education_levels
        self.red_flags = red_flags

    def run(self):
        data_dump = DataDump()
        logger = Logger()
        database = DBEngine()

        # scraping -> creates a compiled data dump from different search parameters
        logger.start_session()  # logging start of a session

        for position in self.positions:
            for company_type in self.company_types:
                for edu_lvl in self.education_levels:
                    logger.start_scraping(position, company_type, edu_lvl)  # logging each scraping attempt
                    try:
                        df = indeed_nl_scraper.get_jobs(position, company_type, edu_lvl)
                    except Exception as inst:
                        logger.error_occurs(inst)
                    else:
                        logger.scraping_result(df)  # logging scraping results
                        data_dump.merge(df)  # merging all values to the data_dump
                    finally:
                        time.sleep(5)  # wait for 5 seconds to avoid a block
                        continue

        # logging scraping results
        logger.scraping_result_final(data_dump.df)

        # data cleansing / formatting
        data_dump.remove_duplicates(field="job_id")  # removing duplicates
        data_dump.add_qualification(red_flags=self.red_flags)  # adding qualification column with True / False

        # adding city id from related SQL table
        data_dump.add_city_id(field="job_loc", cities=database.get_city_id())

        # logging formatted data dump information
        logger.data_formatted(data_dump.df)

        # saving as a csv file
        data_dump.save_to_csv(path="data_dumps/")

        # saving to SQLite DataBase
        data_dump.remove_existent(existent_job_ids=database.get_job_id())  # removing already existent in DB records
        database.insert_jobs(data_dump.df)

        logger.end_session()
        logger.save_to_txt()  # function is yet to be added
