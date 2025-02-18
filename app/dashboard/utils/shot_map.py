# This file contains the function to draw the shot map from raw JSON files

# Necessary imports
from matplotlib import pyplot as plt
from mplsoccer import Pitch

# Import from utilfunc
from utils import open_json, import_fonts
# Import from xG_timeline
from utils import xGTimeline

class shotMap:
    # Constructor
    def __init__(
        self,
        directory: str,
        eventsFile: str,
        xgoalFile: str
    ):
        """
        This class is used to create a shot map.

        :param str directory: The directory where the JSON files are located.
        :param str eventsFile: The name of the events JSON file.
        :param str xgoalFile: The name of the xGoals JSON file.
        """
        self.directory = directory
        self.eventsFile = eventsFile
        self.xgoalFile = xgoalFile

        # Create an instance of the xGTimeline class
        self.xGTimeline = xGTimeline(directory, eventsFile, xgoalFile)

    # Function to draw the shot map
    def plot_shot_map(
        self,
        home_colour: str,
        away_colour: str,
        home_edge_colour: str,
        away_edge_colour: str,
    ) -> plt.Figure:
        """
        This function plots the shot map using matplotlib.

        :params str home_colour: The hex code for the home team's colour (e.g. #FFFFFF for white).
        :params str away_colour: The hex code for the away team's colour (e.g. #FFFFFF for white).
        :params str home_edge_colour: The hex code for the home team's edge colour (e.g. #FFFFFF for white).
        :params str away_edge_colour: The hex code for the away team's edge colour (e.g. #FFFFFF for white).
        """
        # Get the xG data
        xg_data = self.xGTimeline.get_xG_data()
        # Import the fonts
        robotoRegular, robotoBold = import_fonts()

        ## Get the necessary information about the match
        # Open the json file, copy its data, and then immediately close the json file
        jsonData = open_json(self.directory, self.eventsFile)
        # Assign each section of the json file to a variable
        matchInfo = jsonData['matchInfo']
        liveData = jsonData['liveData']
        matchDetails = liveData["matchDetails"]
        # Variables to store the home and away team's scores
        homeScore = matchDetails['scores']['total']['home']
        awayScore = matchDetails['scores']['total']['away']
        # Variable to check the home team
        isHomeTeam = False
        # Get the necessary information about both teams
        for contestant in matchInfo['contestant']:

            if contestant['position'] == 'home':
                homeTeam = contestant['name']
            else:
                if isHomeTeam == False:
                    awayTeam = contestant['name']

        # Create counting variables and categorise the shots
        home_goals = 0
        home_on_target = 0
        home_post = 0
        home_off_target = 0
        home_blocked = 0

        away_goals = 0
        away_on_target = 0
        away_post = 0
        away_off_target = 0
        away_blocked = 0

        # Setup and draw the pitch
        pitch = Pitch(pitch_type='opta', pitch_color='grass', line_color='white',
                    stripe=True)
        fig, ax = pitch.draw(figsize=(10, 8))

        # Go through the xg_data list to get the shots data
        for i in range(0, len(xg_data)):

            # If the shot belongs to a home player...
            if (xg_data['homeScorerName'][i] != ''):

                # Check to see which type of shot it is
                # (16 = goal, 15 = shot on target, 12 = shot blocked,
                # 14 = shot hit post, 13 = shot off target)
                #
                # Then plot the shot location (x, y coordinates) and
                # the size of the shot based on the xG, and increase
                # the counter for the respective type of shot.
                if (xg_data['shotType'][i] == 16):
                    nodes = pitch.scatter(xg_data['x'][i] - ((xg_data['x'][i] - 50.1) * 2), xg_data['y'][i] - ((xg_data['y'][i] - 49.9) * 2), s=700 * xg_data['homeEachXGoal'][i], marker='o',
                                        color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
                    home_goals = home_goals + 1
                    home_on_target = home_on_target + 1
                elif (xg_data['shotType'][i] == 15):
                    nodes = pitch.scatter(xg_data['x'][i] - ((xg_data['x'][i] - 50.1) * 2), xg_data['y'][i] - ((xg_data['y'][i] - 49.9) * 2), s=700 * xg_data['homeEachXGoal'][i], marker='^',
                                        color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
                    home_on_target = home_on_target + 1
                elif (xg_data['shotType'][i] == 14):
                    nodes = pitch.scatter(xg_data['x'][i] - ((xg_data['x'][i] - 50.1) * 2), xg_data['y'][i] - ((xg_data['y'][i] - 49.9) * 2), s=700 * xg_data['homeEachXGoal'][i], marker='s',
                                        color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
                    home_post = home_post + 1
                elif (xg_data['shotType'][i] == 12):
                    nodes = pitch.scatter(xg_data['x'][i] - ((xg_data['x'][i] - 50.1) * 2), xg_data['y'][i] - ((xg_data['y'][i] - 49.9) * 2), s=700 * xg_data['homeEachXGoal'][i], marker='D',
                                        color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
                    home_blocked = home_blocked + 1
                else:
                    nodes = pitch.scatter(xg_data['x'][i] - ((xg_data['x'][i] - 50.1) * 2), xg_data['y'][i] - ((xg_data['y'][i] - 49.9) * 2), s=700 * xg_data['homeEachXGoal'][i], marker='X',
                                        color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
                    home_off_target = home_off_target + 1
            else:
                if (xg_data['shotType'][i] == 16):
                    nodes = pitch.scatter(xg_data['x'][i], xg_data['y'][i], s=700 * xg_data['awayEachXGoal'][i], marker='o',
                                        color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
                    away_goals = away_goals + 1
                    away_on_target = away_on_target + 1
                elif (xg_data['shotType'][i] == 15):
                    nodes = pitch.scatter(xg_data['x'][i], xg_data['y'][i], s=700 * xg_data['awayEachXGoal'][i], marker='^',
                                        color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
                    away_on_target = away_on_target + 1
                elif (xg_data['shotType'][i] == 14):
                    nodes = pitch.scatter(xg_data['x'][i], xg_data['y'][i], s=700 * xg_data['awayEachXGoal'][i], marker='s',
                                        color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
                    away_post = away_post + 1
                elif (xg_data['shotType'][i] == 12):
                    nodes = pitch.scatter(xg_data['x'][i], xg_data['y'][i], s=700 * xg_data['awayEachXGoal'][i], marker='D',
                                        color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
                    away_blocked = away_blocked + 1
                else:
                    nodes = pitch.scatter(xg_data['x'][i], xg_data['y'][i], s=700 * xg_data['awayEachXGoal'][i], marker='X',
                                        color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
                    away_off_target = away_off_target + 1

        # Prepare two strings to store the teams' name, goals scored, and xG
        home_team = homeTeam + ' - ' + \
            str(homeScore) + ' (' + \
            "{:.2f}".format(
                float(xg_data['homeXGoal'][len(xg_data) - 1])) + ' xG)'
        away_team = 'v ' + awayTeam + ' - ' + \
            str(awayScore) + ' (' + \
            "{:.2f}".format(
                float(xg_data['awayXGoal'][len(xg_data) - 1])) + ' xG)'

        # Write the two above strings
        ax.text(49.5, 95, home_team, color=home_colour,
                font_properties=robotoBold, fontsize=20, ha='right')
        ax.text(50.5, 95, away_team, color=away_colour,
                font_properties=robotoBold, fontsize=20, ha='left')

        # Credit
        ax.text(1, 97, "By Daryl - @dgouilard", color='white',
                fontproperties=robotoRegular, fontsize=10)

        # Prepare three text boxes, one for the goal type, two for each team's quantity
        text_box = dict(boxstyle='round', facecolor='white')
        home_values = dict(boxstyle='round', facecolor=home_colour,
                        edgecolor=home_edge_colour)
        away_values = dict(boxstyle='round', facecolor=away_colour,
                        edgecolor=away_edge_colour)

        # Indicate how many goals each team have scored
        ax.text(50, 65, 'Goals', color='black', font_properties=robotoBold,
                fontsize=12, ha='center', bbox=text_box)
        ax.text(39, 65, str(home_goals), color=home_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)
        ax.text(59, 65, str(away_goals), color=away_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=away_values)

        # Indicate how many shots on target (including goals) each team have made
        ax.text(50, 57, 'Shots on target', color='black',
                font_properties=robotoBold, fontsize=12, ha='center', bbox=text_box)
        ax.text(39, 57, str(home_on_target), color=home_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)
        ax.text(59, 57, str(away_on_target), color=away_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=away_values)

        # Indicate how many shots that hit the post each team have made
        ax.text(50, 49, 'Hit post', color='black', font_properties=robotoBold,
                fontsize=12, ha='center', bbox=text_box)
        ax.text(39, 49, str(home_post), color=home_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)
        ax.text(59, 49, str(away_post), color=away_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=away_values)

        # Indicate how many shots off target each team have made
        ax.text(49.85, 41, 'Shots off target', color='black',
                font_properties=robotoBold, fontsize=12, ha='center', bbox=text_box)
        ax.text(39, 41, str(home_off_target), color=home_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)
        ax.text(59, 41, str(away_off_target), color=away_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=away_values)

        # Indicate how many blocked shots each team have made
        ax.text(50, 33, 'Shots blocked', color='black',
                font_properties=robotoBold, fontsize=12, ha='center', bbox=text_box)
        ax.text(39, 33, str(home_blocked), color=home_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)
        ax.text(59, 33, str(away_blocked), color=away_edge_colour,
                font_properties=robotoBold, fontsize=12, ha='left', bbox=away_values)

        # Draw the legends (shape, shot type and xG value) at the bottom of the plot
        ax.text(27, 8, 'Outcomes:', color='white',
                font_properties=robotoBold, fontsize=15, ha='center')
        nodes = pitch.scatter(4, 4, s=300, marker='o',
                            color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
        ax.text(8, 3.25, 'Goal', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        nodes = pitch.scatter(12, 4, s=300, marker='^',
                            color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
        ax.text(17.5, 3.25, 'On target', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        nodes = pitch.scatter(23.5, 4, s=300, marker='s',
                            color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
        ax.text(28.7, 3.25, 'Hit post', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        nodes = pitch.scatter(35, 4, s=300, marker='D',
                            color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
        ax.text(41, 3.25, 'Blocked', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        nodes = pitch.scatter(46.5, 4, s=300, marker='X',
                            color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
        ax.text(52.5, 3.25, 'Off target', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')

        # (The size of the dot increases by the xG value of the shot)
        ax.text(80, 8, 'Dot size increases by the xG value of the shot', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        nodes = pitch.scatter(70.5, 4, s=100, marker='o',
                            color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
        nodes = pitch.scatter(73, 4, s=200, marker='o',
                            color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
        nodes = pitch.scatter(75.8, 4, s=300, marker='o',
                            color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)
        nodes = pitch.scatter(79.2, 4, s=400, marker='o',
                            color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
        nodes = pitch.scatter(83, 4, s=500, marker='o',
                            color=home_colour, edgecolors=home_edge_colour, zorder=1, ax=ax)

        return fig