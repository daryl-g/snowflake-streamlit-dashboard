# This file contains the function to draw the passing network from raw JSON files

# Necessary imports
import matplotlib as mpl

from matplotlib import pyplot as plt
from mplsoccer import Pitch

# Import from utilfunc
from utils import import_fonts
# Import from datafunc
from utils import dataFunc

class passNetwork:
    # Constructor
    def __init__(
        self,
        directory: str,
        passMatrixFile: str,
    ):
        """
        This class creates a passing network from a JSON file.

        :param str directory: The directory where the JSON file is located.
        :param str passMatrixFile: The name of the JSON file.
        """
        self.directory = directory
        self.passMatrixFile = passMatrixFile

        # Create an instance of the dataFunc class
        self.dataFuncs = dataFunc(self.directory, self.passMatrixFile)

    # Function to draw the passing network
    def plot_pass_network(
        self,
        team_colour: str,
        team_edge_colour: str,
        which_team: str = "home",
    ) -> plt.Figure:
        """
        This function plots the passing network using matplotlib.

        :param str team_colour: The hex code for the team's colour (e.g. #FFFFFF for white).
        :param str team_edge_colour: The hex code for the team's edge colour (e.g. #000000 for black).
        :param str which_team: The team to plot the passing network for. Default is "home".

            Options:
                - "home": Home team
                - "away": Away team

        :return plt.Figure: The matplotlib figure object.
        """
        # Check which_team validity
        if which_team not in ["home", "away"]:
            raise ValueError("Invalid team. Please select either 'home' or 'away'.")

        # Import the fonts
        robotoRegular, robotoBold = import_fonts()

        # Access the lineUp section of the json file
        # and get the lineups of both teams
        team_lineUp: list[dict] = self.dataFuncs.get_lineup(which_team)

        # Create a few variables and some arrays to store passing data
        ballPasser = ''
        ballReceiver = ''
        passValue = 0  # Number of passes made to the second player
        player_x_value = 0
        player_y_value = 0

        team_XI = []  # Array to store the team's starting lineup
        team_x_y_values = []  # Array to store the player's x and y values
        team_pass_success = []  # Array to store the player's accurate passes value
        team_pass_location = [] # Array to store the player's x and y values of the pass destination

        # Get the relevant info
        for player in team_lineUp['player']:

            if player['position'] != 'Substitute':

                team_XI.append(player['matchName'])
                player_x_value = player['x']
                player_y_value = player['y']
                team_x_y_values.append(
                    [player['playerId'], player['matchName'], player_x_value, player_y_value])
                team_pass_success.append(player['passSuccess'])

                for playerPass in player['playerPass']:
                    ballPasser = player['playerId']
                    ballReceiver = playerPass['playerId']
                    passValue = playerPass['value']
                    team_pass_location.append(
                        [ballPasser, ballReceiver, passValue])
            else:
                break

        # Setup and draw the pitch
        pitch = Pitch(pitch_type='opta', pitch_color='#0e1117', line_color='white',
                    stripe=False)
        fig, ax = pitch.draw(figsize=(10, 8))

        # Create variables to store the starting and ending x,y coordinates of the passes
        x_start = 0
        y_start = 0
        x_end = 0
        y_end = 0

        for passes in team_pass_location:
            ballPasser = passes[0]
            ballReceiver = passes[1]
            passValue = passes[2]
            for player in team_x_y_values:
                if ballPasser == player[0]:
                    x_start = player[2]
                    y_start = player[3]
                elif ballReceiver == player[0]:
                    x_end = player[2]
                    y_end = player[3]

            if passValue < 4:
                continue
            elif passValue < 6:
                arrow = pitch.arrows(x_start, y_start, x_end, y_end, width=2.5,
                                    headwidth=4, headlength=2, headaxislength=2, color='#c7d5ed', alpha=0.3, ax=ax)
            elif passValue < 12:
                arrow = pitch.arrows(x_start, y_start, x_end, y_end, width=3.5,
                                    headwidth=4, headlength=2, headaxislength=2, color='#abc0e4', alpha=0.5, ax=ax)
            elif passValue < 16:
                arrow = pitch.arrows(x_start, y_start, x_end, y_end, width=4.5,
                                    headwidth=4, headlength=2, headaxislength=2, color='#dde5f4', alpha=0.65, ax=ax)
            else:
                arrow = pitch.arrows(x_start, y_start, x_end, y_end, width=5.5,
                                    headwidth=4, headlength=2, headaxislength=2, color='#f6f8fc', alpha=0.85, ax=ax)

        for i in range(0, len(team_x_y_values)):
            nodes = pitch.scatter(team_x_y_values[i][2], team_x_y_values[i][3], s=4.5 *
                                team_pass_success[i], color=team_colour, edgecolors=team_edge_colour, zorder=1, ax=ax)
            playerInfo = team_XI[i]
            playerPosition = (
                team_x_y_values[i][2], team_x_y_values[i][3])
            text = pitch.annotate(playerInfo, playerPosition, (team_x_y_values[i][2], team_x_y_values[i][3] + 4.2),
                                ha='center', va='center', fontproperties=robotoRegular, fontsize=12, color='white', ax=ax)

        # Create a colour map from the colours used for the arrows
        cmap0 = mpl.colors.LinearSegmentedColormap.from_list(
            'green2red', ['#abc0e4', '#c8d5ed', '#dde5f4', '#f6f8fc'])
        # Set the range of the colour map
        norm = mpl.colors.Normalize(vmin=6, vmax=16)

        # Draw the colour map and set the tick params and the label
        cbar = ax.figure.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap0),
            ax=ax, location='bottom', orientation='horizontal', fraction=.05, pad=0.02)
        cbar.ax.tick_params(color="white", labelcolor="white")
        cbar.set_label('Pass combinations', color='white')

        # Write the note
        ax.text(20, 2, "Size of dot increases by the player's accurate passes",
                color='white', fontsize=10, ha='center')

        # Credit
        ax.text(1, 97, "By Daryl - @dgouilard", color='white',
                fontproperties=robotoRegular, fontsize=10)

        # Set the figure's face colour, width and height
        fig.set_facecolor('#0e1117')
        fig.set_figwidth(10.5)
        fig.set_figheight(10)

        return fig
        