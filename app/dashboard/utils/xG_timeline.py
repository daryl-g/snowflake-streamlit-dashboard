# This file contains the function to draw the xG timeline from raw JSON files

# Necessary imports
import pandas as pd
import matplotlib.patches as patches  # A part of the timeline

from typing import Tuple
from matplotlib import pyplot as plt

# Import from utilfunc
from utils import open_json, import_fonts
# Import from datafunc
from utils import dataFunc

class xGTimeline:
    # Constructor
    def __init__(self, directory: str, eventsFile: str, xgoalFile: str, gap_width: int = 2):
        """
        This class creates an xG timeline from the raw JSON files.

        :param str directory: The directory where the JSON files are located.
        :param str eventsFile: The name of the events JSON file.
        :param str xgoalFile: The name of the xG JSON file.
        :param int gap_width: The width of the gap in between each half. Default is 2.
        """

        # Directory and paths
        self.directory: str = directory
        self.eventsFile: str = eventsFile
        self.xgoalFile: str = xgoalFile

        # Variables to store the length of each half
        self.first_half_time: int = 45
        self.second_half_time: int = 45
        self.first_extra_time: int = 0
        self.second_extra_time: int = 0

        # Determine the width of the gap in between each half
        self.gap_width: int = gap_width

        # Create an instance of the dataFunc class
        self.eventsFuncs = dataFunc(self.directory, self.eventsFile)
        self.xgoalFuncs = dataFunc(self.directory, self.xgoalFile)

    # Function to gather xG data
    def get_xG_data(self) -> pd.DataFrame:
        """
        This function gathers the xG data from the raw JSON files and returns a dataframe.

        :return pd.DataFrame: A dataframe containing the xG data.
        """
        # Open the json file, copy its data, and then immediately close the json file
        eventsData = open_json(self.directory, self.eventsFile)

        # Assign each section of the json file to a variable
        matchInfo = eventsData['matchInfo']
        # Variable to store the number of periods played in the match
        periodNo = self.eventsFuncs.get_num_periods()
        liveData = eventsData['liveData']
        events = liveData['event']

        # For loop to get the end time of each half
        for event in events:

            # Check if the number of periods played is 2 or not
            if (periodNo == 2):

                if (event['typeId'] == 30):
                    if (event['periodId'] == 1):
                        # Get the end time of the first half
                        self.first_half_time = int(event['timeMin'])
                    elif (event['periodId'] == 2):
                        # Get the end time of the second half,
                        self.second_half_time = int(event['timeMin']) - 45
                        # then minus 45 to get the length of the half

            # If the match is played into the extra time (possible due to the Finals series)
            elif (periodNo > 2):

                # Get the end time of the first half of the extra time
                # then minus 90 to get the length of the first extra time
                if (event['typeId'] == 30):
                    if (event['periodId'] == 3):
                        self.first_extra_time = int(event['timeMin']) - 90
                    # Get the end time of the second half of the extra time
                    # then minus 105 (first 90 + first extra time 15) to get the length of the 2nd extra time
                    elif (event['periodId'] == 4):
                        self.second_extra_time = int(event['timeMin']) - 105

        # Open the json file, copy its data, and then immediately close the json file
        xgoalData = open_json(self.directory, self.xgoalFile)

        # Assign each section of the json file to a variable
        # and get the necessary information about the match
        matchInfo = xgoalData['matchInfo']
        liveData = xgoalData['liveData']
        event = liveData['event']

        # Get the necessary information about both teams
        homeTeamId, homeTeam, awayTeamId, awayTeam = self.eventsFuncs.get_team_info()

        # Declare variables to use for data processing
        homeXGoal = 0
        awayXGoal = 0

        # Determine the width of the gap in between each half
        gap_width = 2

        # Create a blank data frame to store the xG data
        xg_data = pd.DataFrame()

        # Create a sample dataset
        xGoalEvent = {
            'minute': 0,  # Minute displayed on the xG timeline
            'realMinute': 0,  # Minute that the shot took place in the match
            'period': 1,  # Period when the shot took place
            'shotType': 0,  # Shot type (assigned by Opta [13, 14, 15, 16])
            'x': 0,  # x coordinate of the shot
            'y': 0,  # y coordinate of the shot
            'homeScorerName': '',  # Name of the goalscorer
            'awayScorerName': '',
            'homeEachXGoal': 0,  # Each shot's expected goal
            'awayEachXGoal': 0,
            'homeXGOT': 0,  # xGOT (Expected goal on target) of each shot
            'awayXGOT': 0,
            'homeXGoal': 0,  # Cumulated expected goal
            'awayXGoal': 0,
        }

        # Add the sample dataset to the data frame
        xg_data = pd.concat([xg_data, pd.DataFrame(
            xGoalEvent, index=[0])], ignore_index=True)

        # Declare variables to store the individual and cumulated expected goals
        homeXGoal = 0
        awayXGoal = 0

        # This loop will go through every shot events in the list.
        # For every shot event...
        for index, event in enumerate(event):

            # Assign the real minute when the shot took place to the dataset
            xGoalEvent['realMinute'] = event['timeMin']

            # Check if the period of the shot event is exceeding 4 or not
            if (event['periodId'] <= 4):

                # Assign the period of the shot to the corresponding column of the dataset
                xGoalEvent['period'] = event['periodId']

                # Calculate the minute which the shot will be displayed in the xG timeline
                # If the shot took place in the first half...
                if (event['periodId'] == 1):
                    # ...assign the usual minute to the corresponding column of the dataset.
                    xGoalEvent['minute'] = event['timeMin']

                # If the shot took place in the second half...
                elif (event['periodId'] == 2):
                    # ...add the length of the stoppage/injury time of the first half (first_half_time - 45)
                    # and the width of the gap to the original minute when the shot took place.
                    xGoalEvent['minute'] = event['timeMin'] + \
                        self.first_half_time - 45 + self.gap_width

                # If the shot took place in the first half of the extra time...
                elif (event['periodId'] == 3):
                    # ...add the length of the stoppage/injury time of the first half *and* the second half
                    # and twice the width of the gap (because there are two gaps separating three halves)
                    # to the original minute when the shot took place.
                    xGoalEvent['minute'] = event['timeMin'] + self.first_half_time - 45 + self.gap_width + \
                        self.second_half_time - 45 + self.gap_width

                # If the shot took place in the second half of the extra time...
                elif (event['periodId'] == 4):
                    # ...add the length of the stoppage/injury time of the first half, the second half
                    # and the first half of the extra time
                    # (first_half_time - 45), (second_half_time - 45) and (first_extra_time - 15)
                    # to the original minute when the shot took place.
                    xGoalEvent['minute'] = event['timeMin'] + self.first_half_time - 45 + self.gap_width + \
                        self.second_half_time - 45 + self.gap_width + self.first_extra_time - 15 + gap_width

            # If the period when the shot took place exceeded 4 (into the penalty shootout)
            # then stop the for loop.
            else:
                break

            # Error with this id
            if (event['id'] == 2207030489):
                break

            # Check if the team in possession's ID matches the home team's ID or not
            if (event['contestantId'] == homeTeamId):

                # Get the typeId of the shot
                xGoalEvent['shotType'] = event['typeId']
                # Get the x coordinate of the shot
                xGoalEvent['x'] = event['x']
                # Get the y coordinate of the shot
                xGoalEvent['y'] = event['y']
                # Assign the scorer's name to the respective value of the dict
                # and leave the away scorer name field blank
                xGoalEvent['homeScorerName'] = event['playerName']
                xGoalEvent['awayScorerName'] = ""

                # Go through the qualifiers of the shot
                for qualifier in event['qualifier']:
                    # If the qualifierId is 321 (store the xG value of the shot)
                    if (qualifier['qualifierId'] == 321):
                        # Get the xG value of the shot
                        xGoalEvent['homeEachXGoal'] = float(
                            qualifier['value'])
                        xGoalEvent['awayEachXGoal'] = 0
                        # Add the xG value of the current shot to the total xG value of the home team
                        homeXGoal += float(qualifier['value'])
                        xGoalEvent['homeXGoal'] = homeXGoal

                    # If the qualifierId is 322 (store the xGOT value of the shot)
                    elif (qualifier['qualifierId'] == 322):
                        # Get the xGOT value of the shot
                        xGoalEvent['homeXGOT'] = float(qualifier['value'])
                        xGoalEvent['awayXGOT'] = 0

                    # Check if the shot (on target) is a blocked shot or not
                    if (qualifier['qualifierId'] == 82):
                        xGoalEvent['shotType'] = 12

            else:

                # Get the typeId of the shot
                xGoalEvent['shotType'] = event['typeId']
                # Get the x coordinate of the shot
                xGoalEvent['x'] = event['x']
                # Get the y coordinate of the shot
                xGoalEvent['y'] = event['y']
                # Assign the scorer's name to the respective value of the dict
                # and leave the home scorer name field blank
                xGoalEvent['homeScorerName'] = ""
                xGoalEvent['awayScorerName'] = event['playerName']

                # Go through the qualifiers of the shot
                for qualifier in event['qualifier']:
                    # If the qualifierId is 321 (store the xG value of the shot)
                    if (qualifier['qualifierId'] == 321):
                        # Get the xG value of the shot
                        xGoalEvent['homeEachXGoal'] = 0
                        xGoalEvent['awayEachXGoal'] = float(
                            qualifier['value'])
                        # Add the xG value of the current shot to the total xG value of the away team
                        awayXGoal += float(qualifier['value'])

                    # If the qualifierId is 322 (store the xGOT value of the shot)
                    elif (qualifier['qualifierId'] == 322):
                        xGoalEvent['homeXGOT'] = 0
                        # Get the xGOT value of the shot
                        xGoalEvent['awayXGOT'] = float(qualifier['value'])

                    # Check if the shot (on target) is a blocked shot or not
                    if (qualifier['qualifierId'] == 82):
                        xGoalEvent['shotType'] = 12

            # Assign the total xG of both teams after this event
            # to the corresponding columns of the dataset.
            xGoalEvent['homeXGoal'] = homeXGoal
            xGoalEvent['awayXGoal'] = awayXGoal

            # Add each event to the big dataframe
            xg_data = pd.concat([xg_data, pd.DataFrame(
                xGoalEvent, index=[0])], ignore_index=True)
            
        # Return the xG data
        return xg_data

    # Function to calculate the figure properties
    def xG_fig_props(self, xg_data: pd.DataFrame) -> Tuple[list, list, list, list, float, int, int]:
        """
        This function calculates the properties of the figure that will be drawn.

        :param pd.DataFrame xg_data: The xG data.

        :return tuple: 
            A tuple containing: 

            - the list of x and y ticks values and labels *(x_times, x_labels, y_times, y_labels)*,

            - the maximum xG value *(max_xg)*,

            - the end time of the graph *(graph_end_time)*,

            - and the time when the last shot was made *(last_shot)*.
        """
        
        # Declare a couple of variables to use
        max_xg = 0
        graph_end_time = 0
        isextratime = False

        # Check if the home team's total xG is larger than the away team's total xG or not...
        # If it is...
        if (xg_data['homeXGoal'].iloc[-1] >= xg_data['awayXGoal'].iloc[-1]):

            # ...then assign the home team's total xG to the max_xg variable.
            # We also round it up to one decimal number because
            # this variable will be used to set the limit of the y axis of our timeline.

            max_xg = round(xg_data['homeXGoal'].iloc[-1], 1)

            # If the match's largest xG is smaller or equal to 2...
            if (max_xg <= 2):
                # ...then create two lists that...
                # ...store the ticks values...
                y_times = [0, 0.25, 0.5, 0.75,
                        1, 1.25, 1.5, 1.75, 2]
                # ...and the ticks labels...
                y_labels = ["0", "0.25", "0.5", "0.75",
                            "1", "1.25", "1.5", "1.75", "2"]
                # to use when drawing the timeline.
            # If the largest xG is larger than 2, but smaller or equal to 3.5...
            elif (max_xg <= 3.5):
                # ...then make these lists slightly less detailed than the previous two.
                y_times = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
                y_labels = ["0", "0.5", "1",
                            "1.5", "2", "2.5", "3", "3.5"]
            else:  # If the largest xG is larger than 3.5...
                # ...then make both lists even less detailed than the previous two.
                y_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                y_labels = ["0", "1", "2", "3", "4",
                            "5", "6", "7", "8", "9", "10"]

        # If the away team's xG is larger than the home team's xG...
        # ...do the same steps for the away team's xG...
        else:
            # ...including assign the away team's total xG to the max_xg variable.
            max_xg = round(xg_data['awayXGoal'].iloc[-1], 1)

            if (max_xg <= 2):
                y_times = [0, 0.25, 0.5, 0.75,
                        1, 1.25, 1.5, 1.75, 2]
                y_labels = ["0", "0.25", "0.5", "0.75",
                            "1", "1.25", "1.5", "1.75", "2"]
            elif (max_xg <= 3.5):
                y_times = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
                y_labels = ["0", "0.5", "1",
                            "1.5", "2", "2.5", "3", "3.5"]
            else:
                y_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                y_labels = ["0", "1", "2", "3", "4",
                            "5", "6", "7", "8", "9", "10"]

        # Calculate the match length
        match_length = self.first_half_time + self.second_half_time + \
            self.first_extra_time + self.second_extra_time

        # Get the time when the last shot was made in this match
        last_shot = xg_data['minute'].iloc[-1]

        # Check if the match is played through to the extra time or not
        if (self.second_extra_time == 0):  # If it is not then...
            # ...calculate the minute that the graph will end by... (it's obvious through the names of the used variables!)
            graph_end_time = match_length + self.gap_width
            isextratime = False
        else:  # If it is played to extra time then do a similar step
            # (gap_width * 3) here is basically because we have three gaps separating the four halves played.
            graph_end_time = match_length + (self.gap_width * 3)
            isextratime = True
        # We also assign the True/False value to the isextratime variable for the code below.

        # Create three variables to store the length and the number of gaps used for each half
        tmp1st = self.first_half_time
        tmp2nd = self.first_half_time + self.gap_width + self.second_half_time
        tmp1et = self.first_half_time + self.gap_width + \
            self.second_half_time + self.gap_width + self.first_extra_time

        # If the match did not play to extra time...
        if (isextratime == False):
            # ...then create these lists to store the ticks values and labels for the x axis.
            # Very similar to what we have done at the start for the y axis.
            x_times = [0, 15, 30, 45, self.first_half_time, self.first_half_time + self.gap_width, self.first_half_time +
                    15 + self.gap_width, self.first_half_time + 30 + self.gap_width, self.first_half_time + 45 + self.gap_width, graph_end_time]
            x_labels = ["", "15", "30", "45", "", "45",
                        "60", "75", "90", str(self.second_half_time + 45)]
        else:
            x_times = [0, 15, 30, 45, tmp1st, tmp1st + self.gap_width, tmp1st +
                    15 + self.gap_width, tmp1st + 30 + self.gap_width, tmp1st + 45 + self.gap_width, tmp2nd,
                    tmp2nd + self.gap_width, tmp1et, tmp1et + self.gap_width, tmp1et + 15 + self.gap_width, graph_end_time]
            x_labels = ["", "15", "30", "45", "", "45", "60",
                        "75", "90", "", "90", "", "105", "", "120"]
            
        # Return the figure properties
        return x_times, x_labels, y_times, y_labels, max_xg, graph_end_time, last_shot

    # Function to plot the xG timeline
    def plot_xG_timeline(
        self,
        home_colour: str,
        away_colour: str,
        home_edge_colour: str,
        away_edge_colour: str,
        bg: str = "white",
        props_colour: str = "white"
    ) -> plt.Figure:
        """
        This function plots the xG timeline.

        :param str home_colour: The hex code for the face colour of the home team (e.g. #FFFFFF for white).
        :param str away_colour: The hex code for the face colour of the away team (e.g. #FFFFFF for white).
        :param str home_edge_colour: The hex code for the edge colour of the home team (e.g. #FFFFFF for white).
        :param str away_edge_colour: The hex code for the edge colour of the away team (e.g. #FFFFFF for white).
        :param str bg: The background colour of the plot. Default is "white". Reminder that the plot is saved with a transparent background.
        :param str props_colour: The colour of the properties. Default is "white".

        :return plt.Figure: The figure of the xG timeline.
        """

        # Get the xG data
        xg_data = self.get_xG_data()
        # Get the figure properties
        x_times, x_labels, y_times, y_labels, max_xg, graph_end_time, last_shot = self.xG_fig_props(xg_data)
        # Import the fonts
        robotoRegular, robotoBold = import_fonts()
        
        # Draw the xG timeline

        ## Get the necessary information about the match
        # Variable to store the number of periods played in the match
        periodNo = self.eventsFuncs.get_num_periods()
        # Variables to store the home and away team's scores
        homeScore, awayScore = self.eventsFuncs.get_scores()
        # Get the necessary information about both teams
        homeTeamId, homeTeam, awayTeamId, awayTeam = self.eventsFuncs.get_team_info()

        # Create the figure to draw the xG timeline
        fig, ax = plt.subplots(figsize=(12, 8))
        # This one is used to remove the outline that connects the plot and the ticks
        plt.box(False)

        # Import the lists of x and y ticks values and labels
        plt.xticks(x_times, x_labels,
                fontproperties=robotoRegular, color=props_colour)
        plt.yticks(y_times, y_labels,
                fontproperties=robotoRegular, color=props_colour)

        # Set the label of the x and y axes
        plt.ylabel("Cumulative Expected Goals (xG)", fontsize=10,
                fontproperties=robotoBold, color=props_colour)
        plt.xlabel("Minutes Played", fontsize=10,
                fontproperties=robotoBold, color=props_colour)

        # Set the limit of the x and y axes
        plt.xlim(0, graph_end_time + 2)
        # Adding two is for creating a small gap to see where the xG lines end
        plt.ylim(0, max_xg + 0.1)

        # Change the properties of the plot's grid and the parameters for the ticks
        plt.grid(zorder=1, color=props_colour, axis='y', alpha=0.2)
        plt.tick_params(axis=u'both', which=u'both', length=0)

        # Add the gaps in between both halves
        rect1 = ax.patch
        rect2 = ax.patch
        rect3 = ax.patch
        rect1 = patches.Rectangle((self.first_half_time, 0), self.gap_width, 10,
                                linewidth=0, edgecolor='white', facecolor=bg, zorder=2)
        rect2 = patches.Rectangle((self.first_half_time + self.gap_width + self.second_half_time, 0), self.gap_width, 10,
                                linewidth=0, edgecolor='white', facecolor=bg, zorder=2)
        rect3 = patches.Rectangle((self.first_half_time + self.gap_width + self.second_half_time + self.gap_width + self.first_extra_time, 0), self.gap_width, 10,
                                linewidth=0, edgecolor='white', facecolor=bg, zorder=2)
        ax.add_patch(rect1)
        if (periodNo > 2):  # Only add the other two patches if there is extra time
            ax.add_patch(rect2)
            ax.add_patch(rect3)
            # Draw the border for the added gaps (extra time gaps)
            ax.axvline(self.first_half_time + self.gap_width + self.second_half_time,
                    color=props_colour, linestyle='-', alpha=0.2)
            ax.axvline(self.first_half_time + self.gap_width + self.second_half_time +
                    self.gap_width, color=props_colour, linestyle='-', alpha=0.2)
            ax.axvline(self.first_half_time + self.gap_width + self.second_half_time + self.gap_width +
                    self.first_extra_time, color=props_colour, linestyle='-', alpha=0.2)
            ax.axvline(self.first_half_time + self.gap_width + self.second_half_time + self.gap_width +
                    self.first_extra_time + self.gap_width, color=props_colour, linestyle='-', alpha=0.2)

        # Draw the borders for the added gaps (gap between two halves)
        ax.axvline(self.first_half_time, color=props_colour,
                linestyle='-', alpha=0.2)
        ax.axvline(self.first_half_time + self.gap_width,
                color=props_colour, linestyle='-', alpha=0.2)

        # Draw the line to indicate the time when the last shot of the match was made
        ax.axvline(last_shot, color=props_colour,
                linestyle='--', alpha=0.2)

        # Draw the steps for each shot event from the xg_data dataframe
        ax.step(x='minute', y='homeXGoal', data=xg_data,
                color=home_colour, linewidth=3, where='post', zorder=1)
        ax.step(x='minute', y='awayXGoal', data=xg_data,
                color=away_colour, linewidth=3, where='post', zorder=1)

        # Continue drawing the xG line until the last minute of the match,
        # rather than stopping at the last shot of the match
        ax.step(x=[graph_end_time, last_shot], y=[xg_data['homeXGoal'][len(xg_data) - 1], xg_data['homeXGoal'][len(xg_data) - 1]],
                color=home_colour, linewidth=3, where='post', zorder=1)
        ax.step(x=[graph_end_time, last_shot], y=[xg_data['awayXGoal'][len(xg_data) - 1], xg_data['awayXGoal'][len(xg_data) - 1]],
                color=away_colour, linewidth=3, where='post', zorder=1)

        # Look for the goalscorer's information in the xg_data dataframe
        for i in range(len(xg_data)):

            # If the shot event has a homeScorerName assigned to it
            # (Essentially if the shot event is a goal and has the goalscorer's name)
            if (xg_data['shotType'][i] == 16) and (xg_data['homeScorerName'][i] != ""):

                # Create a text string which will store the name of the goal scorer and the xG of the goal
                home_text = xg_data['homeScorerName'][i] + "\n" + \
                    "{:.2f}".format(float(xg_data['homeEachXGoal'][i])) + " xG\n" + \
                    "{:.2f}".format(
                        float(xg_data['homeXGOT'][i])) + " xGOT"

                # Create a text box to store the text string
                props = dict(boxstyle='round', facecolor='white',
                            edgecolor=home_colour, alpha=0.7)

                # Plot a dot at the displayed minute when the goal was scored
                ax.scatter(xg_data['minute'][i], xg_data['homeXGoal'][i],
                        s=60, facecolors=home_colour, edgecolors=home_edge_colour, zorder=6, linewidth=3)

                # Display the information of the goal (the text string) within the text box
                ax.text(xg_data['realMinute'][i] + 0.5, xg_data['homeXGoal'][i] + (max_xg / 10 * 0.3), home_text,
                        ha='center', color=home_colour, zorder=6, fontproperties=robotoBold, bbox=props)

            # If the goal is scored by an away player then do the steps similarly,
            # but use the information of the away team.
            elif (xg_data['shotType'][i] == 16) and (xg_data['awayScorerName'][i] != ""):

                away_text = xg_data['awayScorerName'][i] + "\n" + \
                    "{:.2f}".format(float(xg_data['awayEachXGoal'][i])) + " xG\n" + \
                    "{:.2f}".format(
                        float(xg_data['awayXGOT'][i])) + " xGOT"

                props = dict(boxstyle='round', facecolor='white',
                            edgecolor=away_colour, alpha=0.7)

                ax.scatter(xg_data['minute'][i], xg_data['awayXGoal'][i],
                        s=60, facecolors=away_colour, edgecolors=away_edge_colour, zorder=6, linewidth=3)
                ax.text(xg_data['realMinute'][i] + 0.5, xg_data['awayXGoal'][i] + (max_xg / 10 * 0.3), away_text,
                        ha='center', color=away_colour, zorder=6, fontproperties=robotoBold, bbox=props)

        # Determine if each team has scored less/equal to or more than 1 goal
        # to create a text string that stores each team's xG information
        if (homeScore <= 1):
            home_xG = homeTeam + '\n' + \
                str(homeScore) + ' goal\n' + \
                "{:.2f}".format(
                    float(xg_data['homeXGoal'][i])) + ' xG'
        else:
            home_xG = homeTeam + '\n' + \
                str(homeScore) + ' goals\n' + \
                "{:.2f}".format(
                    float(xg_data['homeXGoal'][i])) + ' xG'

        if (awayScore <= 1):
            away_xG = awayTeam + '\n' + \
                str(awayScore) + ' goal\n' + \
                "{:.2f}".format(
                    float(xg_data['awayXGoal'][i])) + ' xG'
        else:
            away_xG = awayTeam + '\n' + \
                str(awayScore) + ' goals\n' + \
                "{:.2f}".format(
                    float(xg_data['awayXGoal'][i])) + ' xG'

        # Add each team's text string to the end of their respective xG line
        home_x_position = graph_end_time + 3
        away_x_position = graph_end_time + 3
        ax.text(home_x_position, xg_data['homeXGoal'][len(xg_data) - 1] - 0.05, home_xG,
                color=home_colour, font_properties=robotoBold, fontsize=15, ha='left')
        ax.text(away_x_position, xg_data['awayXGoal'][len(xg_data) - 1] - 0.05, away_xG,
                color=away_colour, font_properties=robotoBold, fontsize=15, ha='left')

        # Add the text to indicate which half is which
        # (Divide by 2 allows the text to be at the central of its respective space that has been separated by the gap)
        ax.text((self.first_half_time / 2), max_xg + 0.13, 'First half', color=props_colour,
                font_properties=robotoBold, fontsize=15, ha='center')
        ax.text(self.first_half_time + self.gap_width + (self.second_half_time / 2), max_xg + 0.13, 'Second half',
                color=props_colour, font_properties=robotoBold, fontsize=15, ha='center')

        if (periodNo > 2):
            ax.text(self.first_half_time + self.gap_width + self.second_half_time + self.gap_width + (self.first_extra_time / 2), max_xg + 0.13,
                    'First ET', color=props_colour, font_properties=robotoBold, fontsize=15, ha='center')
            ax.text(self.first_half_time + self.gap_width + self.second_half_time + self.gap_width + self.first_extra_time + self.gap_width + (self.second_extra_time / 2), max_xg + 0.13,
                    'Second ET', color=props_colour, font_properties=robotoBold, fontsize=15, ha='center')
            
        return fig