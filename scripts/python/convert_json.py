# This file contains the functions to convert raw JSON files to usable data formats

# Necessary imports
import os
import json
import pandas as pd

class converter:
    # Constructor
    def __init__(
        self,
        data_folder: str
    ):
        """
        Initialise the converter class.

        :param str data_folder: The path to the data directory. 
        
            Options:
            - "2022 World Cup Asian Qualifiers"
            - "AFC Asian Cup 2022"
            - "AFF Cup 2020"
        """
        if data_folder not in ["2022 World Cup Asian Qualifiers", "AFC Asian Cup 2022", "AFF Cup 2020"]:
            raise ValueError("Invalid data folder. Please select from the following options: '2022 World Cup Asian Qualifiers', 'AFC Asian Cup 2022', 'AFF Cup 2020'")
        else:
            self.data_path = "data/" + data_folder + "/"

    # Get the list of files in the data directory
    def get_files(self):
        """
        Get the list of files in the data directory.

        :return: A list of files in the data directory.
        """
        return os.listdir(self.data_path)

    # Import JSON file
    def import_json(self, file_name: str):
        """
        Import a JSON file.

        :param str file_name: The name of the JSON file to import.

        :return: The data from the JSON file.
        """
        with open(self.data_path + file_name, encoding="utf-8", mode="r") as f:
            data = json.load(f)
            # Close the file
            f.close()

        return data
    
    # Convert JSON to DataFrame
    def json_to_df(self, file_type: str = "events"):
        """
        Convert JSON files to a DataFrame.

        :param str file_type: The type of JSON file to convert to a DataFrame.
            
            Options:
            - "events": Event data. Default option.
            - "pass_matrix": Pass network data.
            - "stats": General stats.
            - "xgoal_stats": Expected goal stats.
            - "others": General info.
        """
        # Check if the file type is valid
        if file_type not in ["events", "pass_matrix", "stats", "xgoal_stats", "others"]:
            raise ValueError("Invalid file type. Please select from the following options: 'events', 'pass_matrix', 'stats', 'xgoal_stats'")

        # Get all files in the data directory
        files: list = self.get_files()

        # Retain only the files with the specified file type
        if file_type != "others":
            files: list = [file for file in files if file_type in file]
        else:
            files: list = [file for file in files if "stats" in file]

        # Determine columns based on the file type
        generic_columns: list = [
            "matchId",
            "contestantId",
            "playerId",
        ]
        specific_columns: list = []
        columns: list = []

        if file_type == "events":
            specific_columns: list = [
                "eventId",
                "typeId",
                "outcome",
                "periodId",
                "matchMin",
                "matchSec",
                "eventX",
                "eventY",
                "qualifiers",
                "timeStamp",
            ]

            # Combine generic and specific columns
            columns: list = generic_columns + specific_columns
        elif file_type == "pass_matrix":
            specific_columns: list = [
                "avgX",
                "avgY",
                "passSuccess",
                "passLost",
                "playerPasses",
            ]

            # Combine generic and specific columns
            columns: list = generic_columns + specific_columns
        elif (file_type == "stats") or (file_type == "xgoal_stats"):
            specific_columns: list = [
                "stats",
            ]

            # Combine generic and specific columns
            columns: list = generic_columns + specific_columns
        elif file_type == "others":
            columns: list = [
                # competitions table
                "competitionId",
                "competitionName",
                "competitionCode",
                "competitionAreaId",
                "tournamentCalendarId",
                "tournamentCalendarName",
                "tournamentCalendarStartDate",
                "tournamentCalendarEndDate",
                # contestants table
                "contestantId",
                "contestantName",
                "contestantShortName",
                "contestantOfficialName",
                "contestantCode",
                "contestantCountryId",
                "contestantCountryName",
                # matches_info table
                "matchId",
                "matchDescription",
                "matchDate",
                "matchTime",
                "contestantId1",
                "contestantId2",
                # match_details table
                "matchLengthMin",
                "matchLengthSec",
                "numberOfPeriods",
                "periodLength",
                "overtimeLength",
                "periods",
                "scores",
                # players table
                "playerId",
                "playerKnownName",
                "playerMatchName",
                "playerPosition",
            ]

        # Initialise an empty DataFrame
        df: pd.DataFrame = pd.DataFrame(columns=columns)
        
        # Iterate through all files
        for file in files:
            # Import the JSON file
            data: dict = self.import_json(file)

            # Extract the data
            data: pd.DataFrame = pd.json_normalize(data)

            # Retain only the relevant columns
            data: pd.DataFrame = data[columns]

            # Append the data to the DataFrame
            if file_type != "others":
                df: pd.DataFrame = pd.concat([df, data], ignore_index=True)
            else:
                # Check if the data already exists in the DataFrame
                if df.empty:
                    df: pd.DataFrame = data
                else:
                    # Merge the data with the existing DataFrame
                    df: pd.DataFrame = pd.merge(df, data, on=columns, how="outer")

        return df