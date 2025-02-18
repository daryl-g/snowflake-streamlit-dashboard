# This file contains the functions to extract relevant data from Opta's JSON files.

# Necessary imports
from typing import List, Tuple
from utils import open_json

class dataFunc:
    # Constructor
    def __init__(
        self,
        directory: str,
        jsonFile: str,
    ):
        """
        This class extracts data from Opta's JSON files.

        :param str directory: The directory where the JSON file is located.
        :param str jsonFile: The name of the JSON file.
        """
        self.directory = directory
        self.jsonFile = jsonFile

        # Retrieve the data from the JSON file
        self.jsonData = open_json(self.directory, self.jsonFile)

    # Function to get the team info
    def get_team_info(
        self
    ) -> Tuple[str, str, str, str]:
        """
        This function gets the names of the two teams.

        :return Tuple[str, str]: The IDs and names of the two teams.
        """
        # Get the necessary information about the match
        matchInfo = self.jsonData['matchInfo']

        # Variable to check if the team is the home team
        isHomeTeam = False
        # Get the necessary information about both teams
        for contestant in matchInfo['contestant']:

            if contestant['position'] == 'home':
                homeTeamId = contestant['id']
                homeTeam = contestant['name']
            else:
                if isHomeTeam == False:
                    awayTeamId = contestant['id']
                    awayTeam = contestant['name']

        return homeTeamId, homeTeam, awayTeamId, awayTeam
    
    # Function to get lineUp
    def get_lineup(
        self,
        which_team: str,
    ) -> List[dict]:
        """
        This function gets the lineups of both teams.

        :param str which_team: The team to get the lineup for.

            Options:
                - "home": Home team
                - "away": Away team
                - "both": Both teams

        :return List[dict]: The lineups of both teams.
        """
        # Check which_team validity
        if which_team not in ["home", "away", "both"]:
            raise ValueError("Invalid team. Please select either 'home', 'away', or 'both'.")

        # Access the lineUp section of the json file
        # and get the lineups of both teams
        squadList = self.jsonData['liveData']['lineUp']
        
        # Return data based on which_team
        if which_team == "home":
            return squadList[0]
        elif which_team == "away":
            return squadList[1]
        else:
            return squadList
        
    # Function to get the scores
    def get_scores(
        self,
    ) -> Tuple[int, int]:
        """
        This function gets the scores of the match.

        :return Tuple[int, int]: The scores of the home and away teams.
        """
        # Get the necessary information about the match
        liveData = self.jsonData['liveData']
        matchDetails = liveData['matchDetails']

        # Get the scores of the home and away teams
        homeScore = matchDetails['scores']['total']['home']
        awayScore = matchDetails['scores']['total']['away']

        return homeScore, awayScore
    
    # Function to get the number of periods
    def get_num_periods(
        self,
    ) -> int:
        """
        This function gets the number of periods in the match.

        :return int: The number of periods in the match.
        """
        # Get the necessary information about the match
        matchInfo = self.jsonData['matchInfo']

        # Get the number of periods in the match
        periodNo = int(matchInfo['numberOfPeriods'])

        return periodNo
    
    # Function to get the match name
    def get_match_name(
        self,
    ) -> str:
        """
        This function gets the name of the match.

        :return str: The name of the match.
        """
        # Get the necessary information about the match
        matchInfo = self.jsonData['matchInfo']

        # Get the name of the match
        matchName = matchInfo['description']

        return matchName
    
    # Function to get the competition name
    def get_competition_name(
        self,
    ) -> str:
        """
        This function gets the name of the competition.

        :return str: The name of the competition.
        """
        # Get the necessary information about the match
        matchInfo = self.jsonData['matchInfo']

        # Get the name of the competition
        compName = matchInfo['competition']['name']

        return compName