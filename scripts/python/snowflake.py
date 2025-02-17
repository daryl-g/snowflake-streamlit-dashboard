# This file contains the code to connect to Snowflake and add data to the corresponding tables

# Necessary imports
import pandas as pd
import os

from dotenv import load_dotenv
from snowflake.snowpark import Session
from scripts.python.convert_json import converter

# Load the environment variables
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)

connection_params = {
    "account": os.environ.get("SNOWFLAKE_ACCOUNT"),
    "user": os.environ.get("SNOWFLAKE_USER"),
    "password": os.environ.get("SNOWFLAKE_PASSWORD"),
    "authenticator": os.environ.get("SNOWFLAKE_AUTHENTICATOR"),
    "warehouse": "DASHBOARD_WH",
    "database": "OPTA_DATA",
    "schema": "DATA",
}
session = Session.builder.configs(connection_params).create()


class SnowflakeConnector:
    # Constructor
    def __init__(self):
        pass

    # Function to retrieve data
    def load_data(self, file_type: str, data_folder: str) -> pd.DataFrame:
        """
        This function retrieves the JSON data and converts it to a DataFrame

        :param str file_type: The type of JSON file to convert to a DataFrame.

            Options:
            - "competitions": Competition data.
            - "contestants": Contestant data.
            - "matches": Match data.
            - "match_details": Match details data.
            - "players": Player data.

        :param str data_folder: The folder where the data is stored.

            Options:
            - "2022 World Cup Asian Qualifiers"
            - "AFF Cup 2020"

        :return pd.DataFrame: The DataFrame containing the data.
        """
        # Create a converter object
        conv = converter(data_folder)

        # Get the data
        data: pd.DataFrame = conv.json_to_df(file_type)

        return data

    # Function to inject data into Snowflake
    def inject_data(self):
        """
        This function injects the data into the corresponding tables in Snowflake.
        """
        data_folders: list = [
            "2022 World Cup Asian Qualifiers", "AFF Cup 2020"]
        tables: list = ["competitions", "contestants",
                        "matches_info", "match_details"]

        for folder in data_folders:
            for table in tables:
                # Load the data
                data: pd.DataFrame = self.load_data(
                    table, folder) if table != "matches_info" else self.load_data("matches", folder)

                # Change column names to uppercase
                data.columns = data.columns.str.upper()

                # Fill NULL values with None
                data = data.where(pd.notnull(data), "None")

                # Write the data to the corresponding table
                session.write_pandas(
                    df=data,
                    table_name=table.upper(),
                    database="OPTA_DATA",
                    schema="DATA",
                    auto_create_table=False
                )

                # Drop duplicates from the table
                _ = session.sql(f"create or replace table {table.upper()} as select distinct * from {table.upper()}").collect()

        print("Data has been successfully injected into Snowflake.")
