"""
Functionality for transforming scraping results into a data-dump ready to be uploaded to a DB or saved to .csv
"""
from datetime import datetime
import pandas as pd


class DataDump:
    def __init__(self):
        self.df = pd.DataFrame()

    def merge(self, df):
        """
        Concatenates new df to the datadump

        :param df: pd.DataFrame
        :return: None
        """
        if len(self.df) != 0:
            self.df = pd.concat(objs=[self.df, df])
        else:
            self.df = df

    def remove_duplicates(self, field):
        """
        Removes duplicates from a df by the 'JobID' field.

        :return: None
        """
        self.df.sort_values(by=field, inplace=True)
        self.df.drop_duplicates(subset=[field], keep="first", inplace=True)

    def remove_existent(self, existent_job_ids):
        """
        Removes records that already exist in the SQL database jobs
        :param existent_job_ids: pd.DataFrame
        :return: None
        """

        if existent_job_ids.empty:
            pass
        else:
            self.df["exists"] = self.df["job_id"].isin(existent_job_ids["job_id"])
            self.df = self.df[self.df["exists"] == False]
            self.df.drop("exists", axis=1, inplace=True)

    def add_qualification(self, red_flags):
        """
        Qualifies the jobs as relevant (True) or not (False) based on red flags
        in the position abd job summary fields.
        Adds a qualification results column to the dataframe.

        :param red_flags: list
        :return: None
        """
        red_flags = [flag.lower() for flag in red_flags]

        def flagging(field1, field2):
            for flag in red_flags:
                if (flag in field1.lower()) or (flag in field2.lower()):
                    return False
            return True

        self.df["search_qualified"] = self.df.apply(lambda x: flagging(x.job_title, x.job_summary), axis=1)

    def add_city_id(self, field, cities):
        """
        Extract the exact city, lat and lng from 'job_loc'
        Uses cities_nl table from SQL database with all NL cities.
        Relates DF with id from the cities_nl table
        :return: None
        """

        def find_id(loc):
            for index, city in enumerate(cities["city"]):
                if city in loc:
                    return cities.loc[index, "id"]

        city_ids = self.df[field].apply(find_id)
        self.df.insert(4, "city_id", city_ids)

    def format_salaries(self, field):
        self.df[field] = self.df[field].astype("string")

    def save_to_csv(self, path=None):
        """
        Saves a DataFrame into CSV file
        :param path: string
        :return: None
        """
        suffix = datetime.now().strftime("%d%m%Y_%H%M%S")
        file_name = f"datadump_{suffix}.csv"
        self.df.to_csv(path + file_name, index=False)
