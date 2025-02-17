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
            - "AFF Cup 2020"
        """
        if data_folder not in ["2022 World Cup Asian Qualifiers", "AFF Cup 2020"]:
            raise ValueError(
                "Invalid data folder. Please select from the following options: '2022 World Cup Asian Qualifiers', 'AFF Cup 2020'")
        else:
            self.data_path = "data/" + data_folder + "/"

    # Get the list of files in the data directory
    def get_files(self) -> list:
        """
        Get the list of files in the data directory.

        :return: A list of files in the data directory.
        """
        return os.listdir(self.data_path)

    # Import JSON file
    def import_json(self, file_name: str) -> dict:
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

    # Mapping columns to the flattened JSON
    # Utility function
    def mapping(self, file_type: str, which_way: str = "left", return_dict: bool = False) -> list | dict:
        """
        A utility function to map the columns to the flattened JSON.

        :param str file_type: The type of JSON file to map the columns. Inherited from the json_to_df method.

            Options:
            - "events": Event data.
            - "pass_matrix": Pass network data.
            - "stats": General stats.
            - "xgoal_stats": Expected goal stats.
            - "competitions": Competition data.
            - "contestants": Contestant data.
            - "matches": Match data.
            - "match_details": Match details data.
            - "players": Player data.

        :param str which_way: The direction to map the columns.

            Options:
            - "left": Returns the predefined columns. Default option.
            - "right": Returns the flattened JSON columns.

        :param bool return_dict: Whether to return the mapping as a dictionary. Default is False.
        """

        # Check if the file type is valid
        if file_type not in ["events", "pass_matrix", "stats", "xgoal_stats", "competitions", "contestants", "matches", "match_details", "players"]:
            raise ValueError(
                "Invalid file type. Please select from the following options: 'events', 'pass_matrix', 'stats', 'xgoal_stats'")

        # Check if the direction is valid
        if which_way not in ["left", "right"]:
            raise ValueError(
                "Invalid direction. Please select from the following options: 'left', 'right'")

        # Predefined mappings
        events_columns: dict = {
            "matchId": "matchInfo.id",
            "contestantId": "liveData.event.contestantId",
            "playerId": "liveData.event.playerId",
            "eventId": "liveData.event.eventid",
            "typeId": "liveData.event.typeId",
            "outcome": "liveData.event.outcome",
            "periodId": "liveData.event.periodId",
            "matchMin": "liveData.event.timeMin",
            "matchSec": "liveData.event.timeSec",
            "eventX": "liveData.event.x",
            "eventY": "liveData.event.y",
            "qualifiers": "liveData.event.qualifier",
            "timeStamp": "liveData.event.timeStamp",
        }

        pass_matrix_columns: dict = {
            "matchId": "matchInfo.id",
            "contestantId": "liveData.lineUp.contestantId",
            "playerId": "liveData.lineUp.player.playerId",
            "avgX": "liveData.lineUp.player.x",
            "avgY": "liveData.lineUp.player.y",
            "passSuccess": "liveData.lineUp.player.passSuccess",
            "passLost": "liveData.lineUp.player.passLost",
            "playerPasses": "liveData.lineUp.playerPass",
        }

        playerStats_columns: dict = {
            "matchId": "matchInfo.id",
            "contestantId": "liveData.lineUp.contestantId",
            "playerId": "liveData.lineUp.player.playerId",
            "stats": "liveData.lineUp.player.stat",
        }

        contestantStats_columns: dict = {
            "matchId": "matchInfo.id",
            "contestantId": "liveData.lineUp.contestantId",
            "generalStats": "liveData.lineUp.stat",
            "xgoalStats": "liveData.lineUp.stat",
        }

        xgoal_stats_columns: dict = {
            "matchId": "matchInfo.id",
            "contestantId": "liveData.lineUp.contestantId",
            "playerId": "liveData.lineUp.player.playerId",
            "stats": "liveData.lineUp.player.stat",
        }

        competition_columns: dict = {
            "competitionId": "matchInfo.competition.id",
            "competitionName": "matchInfo.competition.name",
            "competitionCode": "matchInfo.competition.competitionCode",
            "competitionAreaId": "matchInfo.competition.country.id",
            "competitionAreaName": "matchInfo.competition.country.name",
            "tournamentCalendarId": "matchInfo.tournamentCalendar.id",
            "tournamentCalendarName": "matchInfo.tournamentCalendar.name",
            "tournamentCalendarStartDate": "matchInfo.tournamentCalendar.startDate",
            "tournamentCalendarEndDate": "matchInfo.tournamentCalendar.endDate",
        }

        contestant_columns: dict = {
            "contestantId": "matchInfo.contestant.id",
            "contestantName": "matchInfo.contestant.name",
            "contestantShortName": "matchInfo.contestant.shortName",
            "contestantOfficialName": "matchInfo.contestant.officialName",
            "contestantCode": "matchInfo.contestant.code",
            "contestantCountryId": "matchInfo.contestant.country.id",
            "contestantCountryName": "matchInfo.contestant.country.name",
        }

        match_columns: dict = {
            "matchId": "matchInfo.id",
            "matchDescription": "matchInfo.description",
            "matchDate": "matchInfo.date",
            "matchTime": "matchInfo.time",
            "contestantId1": "matchInfo.contestant.id",
            "contestantId2": "matchInfo.contestant.id",
            "competitionId": "matchInfo.competition.id",
            "tournamentCalendarId": "matchInfo.tournamentCalendar.id",
        }

        match_details_columns: dict = {
            "matchId": "matchInfo.id",
            "numberOfPeriods": "matchInfo.numberOfPeriods",
            "periodLength": "matchInfo.periodLength",
            "overtimeLength": "matchInfo.overtimeLength",
            "matchLengthMin": "liveData.matchDetails.matchLengthMin",
            "matchLengthSec": "liveData.matchDetails.matchLengthSec",
            "periods": "liveData.matchDetails.period",
        }

        players_columns: dict = {
            "contestantId": "liveData.lineUp.contestantId",
            "playerId": "liveData.lineUp.player.playerId",
            "playerKnownName": "liveData.lineUp.player.knownName",
            "playerMatchName": "liveData.lineUp.player.matchName",
        }

        # Return the mapping based on the file type
        if file_type == "events":
            if return_dict:
                return events_columns
            else:
                if which_way == "left":
                    return list(events_columns.keys())
                else:
                    return list(events_columns.values())
        elif file_type == "pass_matrix":
            if return_dict:
                return pass_matrix_columns
            else:
                if which_way == "left":
                    return list(pass_matrix_columns.keys())
                else:
                    return list(pass_matrix_columns.values())
        elif file_type == "stats":
            if return_dict:
                return (playerStats_columns, contestantStats_columns)
            else:
                if which_way == "left":
                    return (list(playerStats_columns.keys()), list(contestantStats_columns.keys()))
                else:
                    return (list(playerStats_columns.values()), list(contestantStats_columns.values()))
        elif file_type == "xgoal_stats":
            if return_dict:
                return xgoal_stats_columns
            else:
                if which_way == "left":
                    return list(xgoal_stats_columns.keys())
                else:
                    return list(xgoal_stats_columns.values())
        elif file_type == "competitions":
            if return_dict:
                return competition_columns
            else:
                if which_way == "left":
                    return list(competition_columns.keys())
                else:
                    return list(competition_columns.values())
        elif file_type == "contestants":
            if return_dict:
                return contestant_columns
            else:
                if which_way == "left":
                    return list(contestant_columns.keys())
                else:
                    return list(contestant_columns.values())
        elif file_type == "matches":
            if return_dict:
                return match_columns
            else:
                if which_way == "left":
                    return list(match_columns.keys())
                else:
                    return list(match_columns.values())
        elif file_type == "match_details":
            if return_dict:
                return match_details_columns
            else:
                if which_way == "left":
                    return list(match_details_columns.keys())
                else:
                    return list(match_details_columns.values())
        elif file_type == "players":
            if return_dict:
                return players_columns
            else:
                if which_way == "left":
                    return list(players_columns.keys())
                else:
                    return list(players_columns.values())

    # Traverse the data
    def traverse_data(self, data: str | int | float | list | dict, path_dest: list) -> any:
        """
        Traverse the data and return the required data.

        :param str, int, float, list, dict data: The data from the JSON file.
        :param list path_dest: The path to the required data.

        :return: Any type of data that needs to be returned.
        """
        # Base case: if path_dest is empty, return the data
        if not path_dest:
            return data

        # Get the next key in the path
        key = path_dest[0]

        # Check if the key is a qualifier, stat, scores, period, or playerPass
        if key in ["qualifier", "stat", "scores", "period", "playerPass"]:
            # Go to the next level and return the data
            return [self.traverse_data(data[key], path_dest[1:])]
        # Check the current type of data
        elif isinstance(data, dict):
            # Continue to the next level
            return self.traverse_data(data[key], path_dest[1:])
        elif isinstance(data, list):
            # Empty list to store the extracted data
            extracted_data: list = []
            # Iterate through the list and grab the data that matches the key
            for item in data:
                if key in item:
                    extracted_data.append(
                        self.traverse_data(item[key], path_dest[1:]))
            # Return the extracted data
            return extracted_data
        else:
            # If the data is a primitive type, return it
            return data

    # Convert JSON to DataFrame
    def json_to_df(self, file_type: str = "events") -> pd.DataFrame:
        """
        Convert JSON files to a DataFrame.

        :param str file_type: The type of JSON file to convert to a DataFrame.

            Options:
            - "events": Event data. Default option.
            - "pass_matrix": Pass network data.
            - "stats": General stats.
            - "xgoal_stats": Expected goal stats.
            - "competitions": Competition data.
            - "contestants": Contestant data.
            - "matches": Match data.
            - "match_details": Match details data.
            - "players": Player data.
        """
        # Check if the file type is valid
        if file_type not in ["events", "pass_matrix", "stats", "xgoal_stats", "competitions", "contestants", "matches", "match_details", "players"]:
            raise ValueError(
                "Invalid file type. Please select from the following options: 'events', 'pass_matrix', 'stats', 'xgoal_stats', 'competitions', 'contestants', 'matches', 'match_details', 'players'")

        # Get all files in the data directory
        files: list = self.get_files()

        # Retain only the files with the specified file type
        if file_type not in ["competitions", "contestants", "matches", "match_details", "players"]:
            files: list = [file for file in files if file_type in file]
        else:
            files: list = [file for file in files if "stats" in file]

        # Determine columns based on the file type
        columns: list = self.mapping(file_type, which_way="left")
        json_columns: dict = self.mapping(
            file_type, which_way="right", return_dict=True)

        # Initialise an empty DataFrame
        df: pd.DataFrame = pd.DataFrame(columns=columns)

        # Iterate through all files
        for file in files:
            # Import the JSON file
            data: dict = self.import_json(file)

            # Empty dict to store the extracted data
            data_from_file: dict = {k: "" for k in json_columns.keys()}

            # Empty variable to store the number of values in the dict
            num_values: int = 0

            # Iterate through the JSON columns
            for key, value in json_columns.items():
                # Construct the path
                path_dest: list = value.split(".")

                # Extract the data
                top_level = data[path_dest[0]]
                second_level = top_level[path_dest[1]]

                # Traverse the data
                extracted_data = self.traverse_data(
                    second_level, path_dest[2:])

                # Add the extracted data to the dict
                if ("Date" in key) or ("Time" in key):
                    data_from_file[key] = extracted_data.replace("Z", "")
                elif (key != "contestantId1") and (key != "contestantId2"):
                    data_from_file[key] = extracted_data
                elif key == "contestantId1":
                    data_from_file[key] = extracted_data[0]
                elif key == "contestantId2":
                    data_from_file[key] = extracted_data[1]

                num_values = len(extracted_data) if isinstance(
                    extracted_data, list) else 1

            # Concatenate the mapped data to the main DataFrame
            df = pd.concat(
                [df, pd.DataFrame(data_from_file, index=[i for i in range(0, num_values)])], ignore_index=True)

        # Drop duplicates
        try:
            # Get all ID columns in the DataFrame
            id_columns: list = [
                col for col in df.columns if "Id" in col]

            # Drop duplicates based on the ID columns
            df.drop_duplicates(subset=id_columns, keep="first",
                               inplace=True, ignore_index=True)
        except TypeError:
            pass

        return df
