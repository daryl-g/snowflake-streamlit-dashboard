import streamlit as st
import json  # Use json files
import pandas as pd  # Create DataFrames to store data
import matplotlib as mpl  # Increase quality of the visualisation
import matplotlib.pyplot as plt  # Draw the xG timeline
import matplotlib.patches as patches  # A part of the timeline
import matplotlib.font_manager as fm  # Import fonts

# Draw pitches for the shot map
from snowflake.snowpark import Session
from first_time_setup import render as render_first_time_setup, get_is_first_time_setup_dismissed
from mplsoccer import Pitch

mpl.rcParams['figure.dpi'] = 300

# Global variables
directory = '../../../data/2022 World Cup Asian Qualifiers/'
xgoalFile = 'JPN_VIE_xgoal_stats.json'
eventsFile = 'JPN_VIE_events.json'
passnetworkFile = 'JPN_VIE_pass_matrix.json'
statsFile = 'JPN_VIE_stats.json'

# Import the fonts from the same folder as this code
robotoRegular = fm.FontProperties(fname='./Roboto-Regular.ttf')
robotoBold = fm.FontProperties(fname='./Roboto-Bold.ttf')

# Function to open JSON files


def open_json(directory: str, file: str):
    with open(directory + eventsFile, encoding='utf-8') as jsonFile:
        jsonData = json.load(jsonFile)
        jsonFile.close()

    return jsonData

# Function to create the xG timeline


def xG_timeline(directory: str, xgoalFile: str, eventsFile: str):
    # Variables to store the length of each half
    first_half_time = 45
    second_half_time = 45
    first_extra_time = 0
    second_extra_time = 0

    # Open the json file, copy its data, and then immediately close the json file
    jsonData = open_json(directory, eventsFile)

    # Assign each section of the json file to a variable
    matchInfo = jsonData['matchInfo']
    # Variable to store the number of periods played in the match
    periodNo = int(matchInfo['numberOfPeriods'])
    liveData = jsonData['liveData']
    events = liveData['event']

    # For loop to get the end time of each half
    for event in events:

        # Check if the number of periods played is 2 or not
        if (periodNo == 2):

            if (event['typeId'] == 30):
                if (event['periodId'] == 1):
                    # Get the end time of the first half
                    first_half_time = int(event['timeMin'])
                elif (event['periodId'] == 2):
                    # Get the end time of the second half,
                    second_half_time = int(event['timeMin']) - 45
                    # then minus 45 to get the length of the half

        # If the match is played into the extra time (possible due to the Finals series)
        elif (periodNo > 2):

            # Get the end time of the first half of the extra time
            # then minus 90 to get the length of the first extra time
            if (event['typeId'] == 30):
                if (event['periodId'] == 3):
                    first_extra_time = int(event['timeMin']) - 90
                # Get the end time of the second half of the extra time
                # then minus 105 (first 90 + first extra time 15) to get the length of the 2nd extra time
                elif (event['periodId'] == 4):
                    second_extra_time = int(event['timeMin']) - 105

    # Variable to check the home team
    isHomeTeam = False
    # Open the json file, copy its data, and then immediately close the json file
    jsonData = open_json(directory, xgoalFile)

    # Assign each section of the json file to a variable
    # and get the necessary information about the match
    matchInfo = jsonData['matchInfo']
    liveData = jsonData['liveData']
    matchDetails = liveData["matchDetails"]
    event = liveData['event']
    homeScore = matchDetails['scores']['total']['home']
    awayScore = matchDetails['scores']['total']['away']

    # Get the necessary information about both teams
    for contestant in matchInfo['contestant']:

        if contestant['position'] == 'home':
            homeTeamId = contestant['id']
            homeTeam = contestant['name']
        else:
            if isHomeTeam == False:
                awayTeamId = contestant['id']
                awayTeam = contestant['name']

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
    xg_data = xg_data.append(xGoalEvent, ignore_index=True)

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
                    first_half_time - 45 + gap_width

            # If the shot took place in the first half of the extra time...
            elif (event['periodId'] == 3):
                # ...add the length of the stoppage/injury time of the first half *and* the second half
                # and twice the width of the gap (because there are two gaps separating three halves)
                # to the original minute when the shot took place.
                xGoalEvent['minute'] = event['timeMin'] + first_half_time - 45 + gap_width + \
                    second_half_time - 45 + gap_width

            # If the shot took place in the second half of the extra time...
            elif (event['periodId'] == 4):
                # ...add the length of the stoppage/injury time of the first half, the second half
                # and the first half of the extra time
                # (first_half_time - 45), (second_half_time - 45) and (first_extra_time - 15)
                # to the original minute when the shot took place.
                xGoalEvent['minute'] = event['timeMin'] + first_half_time - 45 + gap_width + \
                    second_half_time - 45 + gap_width + first_extra_time - 15 + gap_width

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
        xg_data = xg_data.append(xGoalEvent, ignore_index=True)

        home_colour = 'darkblue'
        home_edge_colour = 'white'

        away_colour = 'red'
        away_edge_colour = 'yellow'

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
        match_length = first_half_time + second_half_time + \
            first_extra_time + second_extra_time

        # Get the time when the last shot was made in this match
        last_shot = xg_data['minute'].iloc[-1]

        # Check if the match is played through to the extra time or not
        if (second_extra_time == 0):  # If it is not then...
            # ...calculate the minute that the graph will end by... (it's obvious through the names of the used variables!)
            graph_end_time = match_length + gap_width
            isextratime = False
        else:  # If it is played to extra time then do a similar step
            # (gap_width * 3) here is basically because we have three gaps separating the four halves played.
            graph_end_time = match_length + (gap_width * 3)
            isextratime = True
        # We also assign the True/False value to the isextratime variable for the code below.

        # Create three variables to store the length and the number of gaps used for each half
        tmp1st = first_half_time
        tmp2nd = first_half_time + gap_width + second_half_time
        tmp1et = first_half_time + gap_width + \
            second_half_time + gap_width + first_extra_time

        # If the match did not play to extra time...
        if (isextratime == False):
            # ...then create these lists to store the ticks values and labels for the x axis.
            # Very similar to what we have done at the start for the y axis.
            x_times = [0, 15, 30, 45, first_half_time, first_half_time + gap_width, first_half_time +
                       15 + gap_width, first_half_time + 30 + gap_width, first_half_time + 45 + gap_width, graph_end_time]
            x_labels = ["", "15", "30", "45", "", "45",
                        "60", "75", "90", str(second_half_time + 45)]
        else:
            x_times = [0, 15, 30, 45, tmp1st, tmp1st + gap_width, tmp1st +
                       15 + gap_width, tmp1st + 30 + gap_width, tmp1st + 45 + gap_width, tmp2nd,
                       tmp2nd + gap_width, tmp1et, tmp1et + gap_width, tmp1et + 15 + gap_width, graph_end_time]
            x_labels = ["", "15", "30", "45", "", "45", "60",
                        "75", "90", "", "90", "", "105", "", "120"]

        # Choose the background colour for the timeline and the stripes colour for the shots map
        bg = "white"
        # stripe_colour = '#bf4789'

        # Draw the xG timeline:

        # Create the figure to draw the xG timeline
        fig, ax = plt.subplots(figsize=(12, 8))
        # This one is used to remove the outline that connects the plot and the ticks
        plt.box(False)

        # Import the lists of x and y ticks values and labels
        plt.xticks(x_times, x_labels,
                   fontproperties=robotoRegular, color="black")
        plt.yticks(y_times, y_labels,
                   fontproperties=robotoRegular, color="black")

        # Set the label of the x and y axes
        plt.ylabel("Cumulative Expected Goals (xG)", fontsize=10,
                   fontproperties=robotoBold, color="black")
        plt.xlabel("Minutes Played", fontsize=10,
                   fontproperties=robotoBold, color="black")

        # Set the limit of the x and y axes
        plt.xlim(0, graph_end_time + 2)
        # Adding two is for creating a small gap to see where the xG lines end
        plt.ylim(0, max_xg + 0.1)

        # Change the properties of the plot's grid and the parameters for the ticks
        plt.grid(zorder=1, color="black", axis='y', alpha=0.2)
        plt.tick_params(axis=u'both', which=u'both', length=0)

        # Add the gaps in between both halves
        rect1 = ax.patch
        rect2 = ax.patch
        rect3 = ax.patch
        rect1 = patches.Rectangle((first_half_time, 0), gap_width, 10,
                                  linewidth=0, edgecolor='white', facecolor=bg, zorder=2)
        rect2 = patches.Rectangle((first_half_time + gap_width + second_half_time, 0), gap_width, 10,
                                  linewidth=0, edgecolor='white', facecolor=bg, zorder=2)
        rect3 = patches.Rectangle((first_half_time + gap_width + second_half_time + gap_width + first_extra_time, 0), gap_width, 10,
                                  linewidth=0, edgecolor='white', facecolor=bg, zorder=2)
        ax.add_patch(rect1)
        if (periodNo > 2):  # Only add the other two patches if there is extra time
            ax.add_patch(rect2)
            ax.add_patch(rect3)
            # Draw the border for the added gaps (extra time gaps)
            ax.axvline(first_half_time + gap_width + second_half_time,
                       color='black', linestyle='-', alpha=0.2)
            ax.axvline(first_half_time + gap_width + second_half_time +
                       gap_width, color='black', linestyle='-', alpha=0.2)
            ax.axvline(first_half_time + gap_width + second_half_time + gap_width +
                       first_extra_time, color='black', linestyle='-', alpha=0.2)
            ax.axvline(first_half_time + gap_width + second_half_time + gap_width +
                       first_extra_time + gap_width, color='black', linestyle='-', alpha=0.2)

        # Draw the borders for the added gaps (gap between two halves)
        ax.axvline(first_half_time, color='black',
                   linestyle='-', alpha=0.2)
        ax.axvline(first_half_time + gap_width,
                   color='black', linestyle='-', alpha=0.2)

        # Draw the line to indicate the time when the last shot of the match was made
        ax.axvline(last_shot, color='black',
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
        ax.text((first_half_time / 2), max_xg + 0.13, 'First half', color='black',
                font_properties=robotoBold, fontsize=15, ha='center')
        ax.text(first_half_time + gap_width + (second_half_time / 2), max_xg + 0.13, 'Second half',
                color='black', font_properties=robotoBold, fontsize=15, ha='center')

        if (periodNo > 2):
            ax.text(first_half_time + gap_width + second_half_time + gap_width + (first_extra_time / 2), max_xg + 0.13,
                    'First ET', color='black', font_properties=robotoBold, fontsize=15, ha='center')
            ax.text(first_half_time + gap_width + second_half_time + gap_width + first_extra_time + gap_width + (second_extra_time / 2), max_xg + 0.13,
                    'Second ET', color='black', font_properties=robotoBold, fontsize=15, ha='center')

    # Ask Streamlit to show the viz
    st.pyplot(fig)

# Function to create the shot map
def shot_map(directory: str, eventsFile: str):
    # Open the json file, copy its data, and then immediately close the json file
    jsonData = open_json(directory, eventsFile)

    # Assign each section of the json file to a variable
    matchInfo = jsonData['matchInfo']
    # Variable to store the number of periods played in the match
    periodNo = int(matchInfo['numberOfPeriods'])
    liveData = jsonData['liveData']
    events = liveData['event']

    # For loop to get the end time of each half
    for event in events:

        # Check if the number of periods played is 2 or not
        if (periodNo == 2):

            if (event['typeId'] == 30):
                if (event['periodId'] == 1):
                    # Get the end time of the first half
                    first_half_time = int(event['timeMin'])
                elif (event['periodId'] == 2):
                    # Get the end time of the second half,
                    second_half_time = int(event['timeMin']) - 45
                    # then minus 45 to get the length of the half

        # If the match is played into the extra time (possible due to the Finals series)
        elif (periodNo > 2):

            # Get the end time of the first half of the extra time
            # then minus 90 to get the length of the first extra time
            if (event['typeId'] == 30):
                if (event['periodId'] == 3):
                    first_extra_time = int(event['timeMin']) - 90
                # Get the end time of the second half of the extra time
                # then minus 105 (first 90 + first extra time 15) to get the length of the 2nd extra time
                elif (event['periodId'] == 4):
                    second_extra_time = int(event['timeMin']) - 105

    # Variable to check the home team
    isHomeTeam = False
    # Open the json file, copy its data, and then immediately close the json file
    jsonData = open_json(directory, xgoalFile)

    # Assign each section of the json file to a variable
    # and get the necessary information about the match
    matchInfo = jsonData['matchInfo']
    liveData = jsonData['liveData']
    matchDetails = liveData["matchDetails"]
    event = liveData['event']
    homeScore = matchDetails['scores']['total']['home']
    awayScore = matchDetails['scores']['total']['away']

    # Get the necessary information about both teams
    for contestant in matchInfo['contestant']:

        if contestant['position'] == 'home':
            homeTeamId = contestant['id']
            homeTeam = contestant['name']
        else:
            if isHomeTeam == False:
                awayTeamId = contestant['id']
                awayTeam = contestant['name']

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
    xg_data = xg_data.append(xGoalEvent, ignore_index=True)

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
                    first_half_time - 45 + gap_width

            # If the shot took place in the first half of the extra time...
            elif (event['periodId'] == 3):
                # ...add the length of the stoppage/injury time of the first half *and* the second half
                # and twice the width of the gap (because there are two gaps separating three halves)
                # to the original minute when the shot took place.
                xGoalEvent['minute'] = event['timeMin'] + first_half_time - 45 + gap_width + \
                    second_half_time - 45 + gap_width

            # If the shot took place in the second half of the extra time...
            elif (event['periodId'] == 4):
                # ...add the length of the stoppage/injury time of the first half, the second half
                # and the first half of the extra time
                # (first_half_time - 45), (second_half_time - 45) and (first_extra_time - 15)
                # to the original minute when the shot took place.
                xGoalEvent['minute'] = event['timeMin'] + first_half_time - 45 + gap_width + \
                    second_half_time - 45 + gap_width + first_extra_time - 15 + gap_width

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
        xg_data = xg_data.append(xGoalEvent, ignore_index=True)

        home_colour = 'darkblue'
        home_edge_colour = 'white'

        away_colour = 'red'
        away_edge_colour = 'yellow'

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
                  stripe=True, constrained_layout=True, tight_layout=True)
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

    # Ask Streamlit to show the viz
    st.pyplot(fig)

# Function to create the passing network
def passing_network(directory: str, eventsFile: str):
    isHomeTeam = False
    # Open the json file, copy its data, and then immediately close the json file
    jsonData = open_json(directory, eventsFile)

    # Assign each section of the json file to a variable
    # and get the necessary information about the match
    matchInfo = jsonData['matchInfo']
    matchName = matchInfo['description']
    compName = matchInfo['competition']['name']
    liveData = jsonData['liveData']
    matchDetails = liveData["matchDetails"]
    homeScore = matchDetails['scores']['total']['home']
    awayScore = matchDetails['scores']['total']['away']

    # Get the necessary information about both teams
    for contestant in matchInfo['contestant']:

        if contestant['position'] == 'home':
            homeTeamId = contestant['id']
            homeTeam = contestant['name']
        else:
            if isHomeTeam == False:
                awayTeamId = contestant['id']
                awayTeam = contestant['name']

    # Access the lineUp section of the json file
    # and get the lineups of both teams
    liveData = jsonData['liveData']
    squadList = liveData['lineUp']
    home = squadList[0]
    away = squadList[1]

    # Create a few variables and some arrays to store passing data
    ballPasser = ''
    ballReceiver = ''
    passValue = 0  # Number of passes made to the second player
    player_x_value = 0
    player_y_value = 0
    homeXI = []  # Array to store the home team's starting lineup
    awayXI = []  # Array to store the away team's starting lineup
    home_x_y_values = []  # Array to store the home player's x and y values
    away_x_y_values = []  # Array to store the away player's x and y values
    home_pass_success = []  # Array to store the home player's accurate passes value
    away_pass_success = []  # Array to store the away player's accurate passes value
    # Array to store the home player's x and y values of the pass destination
    homePassLocation = []
    # Array to store the away player's x and y values of the pass destination
    awayPassLocation = []

    # Do the same process as above for the away team
    for player in away['player']:

        if player['position'] != 'Substitute':

            awayXI.append(player['matchName'])
            player_x_value = player['x']
            player_y_value = player['y']
            away_x_y_values.append(
                [player['playerId'], player['matchName'], player_x_value, player_y_value])
            away_pass_success.append(player['passSuccess'])

            for playerPass in player['playerPass']:
                ballPasser = player['playerId']
                ballReceiver = playerPass['playerId']
                passValue = playerPass['value']
                awayPassLocation.append(
                    [ballPasser, ballReceiver, passValue])
        else:
            break

    home_colour = 'darkblue'
    home_edge_colour = 'white'

    away_colour = 'red'
    away_edge_colour = 'yellow'

    # Setup and draw the pitch
    pitch = Pitch(pitch_type='opta', pitch_color='#0e1117', line_color='white',
                  stripe=False, constrained_layout=True, tight_layout=True)
    fig, ax = pitch.draw(figsize=(10, 8))

    # Create variables to store the starting and ending x,y coordinates of the passes
    x_start = 0
    y_start = 0
    x_end = 0
    y_end = 0

    for passes in awayPassLocation:
        ballPasser = passes[0]
        ballReceiver = passes[1]
        passValue = passes[2]
        for player in away_x_y_values:
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

    for i in range(0, len(away_x_y_values)):
        nodes = pitch.scatter(away_x_y_values[i][2], away_x_y_values[i][3], s=4.5 *
                              away_pass_success[i], color=away_colour, edgecolors=away_edge_colour, zorder=1, ax=ax)
        playerInfo = awayXI[i]
        playerPosition = (
            away_x_y_values[i][2], away_x_y_values[i][3])
        text = pitch.annotate(playerInfo, playerPosition, (away_x_y_values[i][2], away_x_y_values[i][3] + 4.2),
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

    # Ask Streamlit to plot the figure
    st.pyplot(fig)

# Function to render the page


def render(session: Session):
    # Set the title of the page
    st.title("How to read football vizzes")
    st.markdown("This instructions page will try its best to help you read the football visualisations (I like to call them vizzes!) that is freshly baked, made and used in this app!")

    userOption = st.selectbox(
        label="Choose visualisation to be displayed",
        options=("xG timeline",
                 "Shot map",
                 "Passing network"),
        index=0
    )

    # A wish to the user while they are waiting for the viz
    with st.spinner("Hope you are having a good day! These instructions will be with you shortly."):

        if (userOption == 'xG timeline'):

            # Create the xG timeline
            xG_timeline(
                directory=directory,
                xgoalFile=xgoalFile,
                eventsFile=eventsFile
            )

            # Instructions to read the xG timeline
            st.subheader(
                "What is the purpose of the xG timeline?"
            )
            st.markdown(
                "The purpose of the xG timeline (or xG match story, as on Football Manager 2021 and 2022) is to tell the story of the match through both teams' cumulated expected goals. For each chance that either team created, their total xG will be increased by the xG value of the shot that they have created."
            )
            st.markdown(
                "From the xG timeline, it is possible to see which team have created more dangerous chances, and which team have dominated the match, and during which period."
            )
            st.markdown(
                "There will be matches where one team finished the match with more xG than their opposition, yet they were the losing team. It could be due to that team were unable to convert their chances, and their opposition managed to take the few chances that they had."
            )

            st.subheader(
                "What is in an xG timeline like the one above?"
            )
            st.markdown(
                "Firstly, the most important thing which is both teams' total xG value throughout the match. It is represented by two different colours, and ended with a title that says which team does the xG line belongs to, how many goals have they scored, and what is that team's total xG value."
            )
            st.markdown(
                "Secondly, the xG timeline also distinctively separates both halves of the match and, potentially, includes both halves of the extra time. Each halves will be distinguished by a small gap in between the two halves."
            )
            st.markdown(
                "Thirdly, depending on the creator of the xG timeline, but usually there will be a dotted line that shows the end of the match. The dotted line in the xG timeline above shows the last shot of the match, not the end of the match. But usually, the dotted line can be close to or even right at the end of the match."
            )

            st.subheader(
                "How to read the xG timeline?"
            )
            st.markdown(
                "Each step on each team's xG line indicates a chance was created during that point in the match. The more steps, the more chances one team created. The bigger the steps, the higher the quality/scoring probability of the created chance."
            )
            st.markdown(
                "Each dot on each team's xG line indicates a goal was scored from the created chance. The information of the goal scorer, Opta's xG and xGOT (Expected Goals on Target) values of the goal will be displayed over the dot. One team can have no dot on their xG line, which indicates that they have not scored any goal."
            )

            st.markdown(
                "Obviously, my explanation won't be the most detailed explanation ever. But you can read more about xG and xGOT from these articles below by Opta's The Analyst!"
            )
            st.markdown(
                "https://theanalyst.com/eu/2021/07/what-are-expected-goals-xg/"
            )
            st.markdown(
                "https://theanalyst.com/eu/2021/06/what-are-expected-goals-on-target-xgot/"
            )

        if (userOption == 'Shot map'):

            # Create the shot map
            # shot_map(
            #     directory=directory,
            #     eventsFile=eventsFile
            # )

            # Instructions to read the shot map
            st.subheader(
                "What is the purpose of a shot map?"
            )
            st.markdown(
                "The purpose of a shot map is to show the position of the shots taken during the match on a 2D canvas, and the xG values of the shots."
            )
            st.markdown(
                "A shot map can be helpful for pointing out the shooting pattern of a team, whether a team prefer to make long shots from outside of the box or try to work their way into the box. It is also useful to point out the vulnerable defending areas of a team based on which area on the pitch that they have conceded the most shots."
            )
            st.markdown(
                "A shot map can also be used to see how dangerous a team were in the match through the xG values of their created chances, and where on the pitch did one team create more dangerous chances."
            )

            st.subheader(
                "What is included in a shot map?"
            )
            st.markdown(
                "Both teams' attempted shots, obviously! But in order to specify the type of each shot, there can be many symbols used to represent different types of shot, which is listed in the **Outcomes** section at the bottom."
            )
            st.markdown(
                "The size of each shot also represents the xG value of that shot. The bigger the dot is, the higher the xG value of that shot is. This does not mean that a goal always have a high xG value."
            )
            st.markdown(
                "And the total number of shots for each type, listed in the middle of the pitch!"
            )

            st.subheader(
                "How to read a shot map?"
            )
            st.markdown(
                "Both teams' shot will be located at two different ends of the pitch, with the shots made by the home side on the left, and the away side on the right, no matter of which side of the pitch they started first."
            )
            st.markdown(
                "As mentioned, each dot on the pitch represents the location where the shot was taken. The size of the dot represents the probability of scoring (xG) of a shot."
            )

        elif (userOption == 'Passing network'):

            # Create the passing network
            # passing_network(
            #     directory=directory,
            #     eventsFile=eventsFile
            # )

            # Instructions on how to read a passing network
            st.subheader(
                "What is the purpose of a passing network?"
            )
            st.markdown(
                "Passing networks can be used to study and analyse a team's passing trends and patterns in a match. Between two players, they are connected through a line that represents how many passes were made from one player to the other in a match."
            )
            st.markdown(
                "It is useful in team and opposition analysis, as it is possible to notice which player has the most influence (received and made the most passes) and which player(s) is dangerous when he has the ball (made more passes than other players)."
            )
            st.markdown(
                "From such decisions, teams can adjust their style of play to press particular players or attempt to minimise the influence of a player in a match by preventing that player from making or receiving passes."
            )

            st.subheader(
                "What is included in a passing network?"
            )
            st.markdown(
                "Firstly, 11 nodes represent 11 starting players of a team. Some passing networks will position the players based on their position, but in most passing networks, the nodes also represent the average position of a player when he receives the ball."
            )
            st.markdown(
                "Secondly, the passes made in between two players are usually represented by two arrows. The brighter and thicker the arrows in the passing network above, the higher the number of passes was made from one player to the other in the match, and vice versa."
            )
            st.markdown(
                "Thirdly, the size of the player's node represents the number of successful/accurate passes made by that player in the match."
            )

            st.subheader(
                "How to read a passing network?"
            )
            st.markdown(
                "The position of the players give us a good view of which formation the team were using when they had the ball in the match."
            )
            st.markdown(
                "Usually, the thickness of the pass connections will indicate a team's on ball preference. It is possible to see the team's preferred attacking side (left wing, right wing, down the central area), which player was the focus of the team (received and made more passes),..."
            )
            st.markdown(
                "By no means are my explanation is thorough. But I highly recommend this article by Karun Singh, who is one of the best researcher in football analytics, if you are interested in finding out more: https://karun.in/blog/interactive-passing-networks.html."
            )


if __name__ == "__main__":
    session = Session.builder.getOrCreate()
    if not get_is_first_time_setup_dismissed(session):
        render_first_time_setup(session)
    else:
        render(session)
