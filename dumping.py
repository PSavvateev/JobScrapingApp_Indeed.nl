"""
Functionality for transforming scraping results into a data-dump ready to be uploaded to a DB or saved to .csv
"""
from datetime import datetime
import pandas as pd
import ast


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

    def date_fields_format(self, fields):
        """
        Formats fields to datetime type.

        :return: None
        """
        for field in fields:
            self.df[field] = pd.to_datetime(self.df[field], infer_datetime_format=True)

    def remove_duplicates(self, field):
        """
        Removes duplicates from a df by the 'JobID' field.

        :return: None
        """
        self.df.sort_values(by=field, inplace=True)
        self.df.drop_duplicates(subset=[field], keep="first", inplace=True)

    def add_qualification(self, red_flags):
        """
        Qualifies the jobs as relevant (True) or not (False) based on red flags in the summary field.
        Adds a qualification results column to the dataframe.

        :param red_flags: list
        :return: None
        """
        red_flags = [flag.lower() for flag in red_flags]
        field = "job_summary"

        def flagging(summary):
            for flag in red_flags:
                if flag in summary.lower():
                    return False
            return True

        self.df["search_qualified"] = self.df[field].apply(flagging)

    def add_job_city(self, field, nl_path):
        """
        Extract the exact city, lat and lng from 'job_loc'
        Uses external nl.csv dataset with all NL cities.
        Adds extra columns to the DF.
        :return: None
        """

        nl = pd.read_csv(nl_path)

        def find_city(loc):
            for city in nl["city"]:
                if city in loc:
                    return city

        def find_lat(loc):
            for index, city in enumerate(nl["city"]):
                if city == loc:
                    return nl.loc[index, "lat"]

        def find_lng(loc):
            for index, city in enumerate(nl["city"]):
                if city == loc:
                    return nl.loc[index, "lng"]

        job_cities = self.df[field].apply(find_city)
        self.df.insert(4, "job_city", job_cities)

        job_lats = self.df["job_city"].apply(find_lat)
        self.df.insert(5, "job_lat", job_lats)

        job_lngs = self.df["job_city"].apply(find_lng)
        self.df.insert(5, "job_lng", job_lngs)

    def format_salaries(self, field):
        self.df[field].fillna("[]", inplace=True)
        self.df[field] = self.df[field].apply(ast.literal_eval)

    def save_to_csv(self, path=None):
        """
        Saves a DataFrame into CSV file
        :param path: string
        :return: None
        """
        suffix = datetime.now().strftime("%d%m%Y_%H%M%S")
        file_name = f"datadump_{suffix}.csv"
        self.df.to_csv(path+file_name, index=False)

