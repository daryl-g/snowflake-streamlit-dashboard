import streamlit as st
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm
from mplsoccer import Pitch, VerticalPitch
mpl.rcParams['figure.dpi'] = 300

# Page title
st.title("Player's performance")

col1, col2 = st.columns(2)

with col1:
    
    # Select box to choose competition
    competitionOption = st.radio(
        label='Choose competition',
        options=('2022 World Cup Asian Qualifiers',
                    'AFF Cup 2020'),
        index=0
    )

    if (competitionOption == '2022 World Cup Asian Qualifiers'):
        # Select box to choose current displaying match
        matchOption = st.selectbox(
            label='Choose match to display visualisations',
            options=('3 September 2021 - Saudi Arabia 3-1 Vietnam',
                        '7 September 2021 - Vietnam 0-1 Australia',
                        '8 October 2021 - China 3-2 Vietnam',
                        '13 October 2021 - Oman 3-1 Vietnam',
                        '11 November 2021 - Vietnam 0-1 Japan',
                        '16 November 2021 - Vietnam 0-1 Saudi Arabia',
                        '27 January 2022 - Australia 4-0 Vietnam',
                        '1 February 2022 - Vietnam 3-1 China',
                        '24 March 2022 - Vietnam 0-1 Oman',
                        '29 March 2022 - Japan 1-1 Vietnam'),
            index=0
        )
    elif (competitionOption == 'AFF Cup 2020'):
        matchOption = st.selectbox(
            label='Choose match to display visualisations',
            options=('6 December 2021 - Laos 0-2 Vietnam',
                        '12 December 2021 - Vietnam 3-0 Malaysia',
                        '15 December 2021 - Indonesia 0-0 Vietnam',
                        '19 December 2021 - Vietnam 4-0 Cambodia',
                        '23 December 2021 - Vietnam 0-2 Thailand',
                        '26 December 2021 - Thailand 0-0 Vietnam'),
            index=0
        )

    # Assign json files that belong to the chosen match
    xgoalFile = ''
    eventsFile = ''
    statsFile = ''

    if (competitionOption == '2022 World Cup Asian Qualifiers'):
        directory = 'data/2022 World Cup Asian Qualifiers/'

        if (matchOption == '3 September 2021 - Saudi Arabia 3-1 Vietnam'):
            xgoalFile = 'KSA_VIE_xgoal.json'
            eventsFile = 'KSA_VIE_events.json'
            statsFile = 'KSA_VIE_stats.json'
        elif (matchOption == '7 September 2021 - Vietnam 0-1 Australia'):
            xgoalFile = 'VIE_AUS_xgoal.json'
            eventsFile = 'VIE_AUS_events.json'
            statsFile = 'VIE_AUS_stats.json'
        elif (matchOption == '8 October 2021 - China 3-2 Vietnam'):
            xgoalFile = 'CHN_VIE_xgoal.json'
            eventsFile = 'CHN_VIE_events.json'
            statsFile = 'CHN_VIE_stats.json'
        elif (matchOption == '13 October 2021 - Oman 3-1 Vietnam'):
            xgoalFile = 'OMA_VIE_xgoal_stats.json'
            eventsFile = 'OMA_VIE_events.json'
            statsFile = 'OMA_VIE_stats.json'
        elif (matchOption == '11 November 2021 - Vietnam 0-1 Japan'):
            xgoalFile = 'VIE_JPN_xgoal_stats.json'
            eventsFile = 'VIE_JPN_events.json'
            statsFile = 'VIE_JPN_stats.json'
        elif (matchOption == '16 November 2021 - Vietnam 0-1 Saudi Arabia'):
            xgoalFile = 'VIE_KSA_xgoal_stats.json'
            eventsFile = 'VIE_KSA_events.json'
            statsFile = 'VIE_KSA_stats.json'
        elif (matchOption == '27 January 2022 - Australia 4-0 Vietnam'):
            xgoalFile = 'AUS_VIE_xgoal_stats.json'
            eventsFile = 'AUS_VIE_events.json'
            statsFile = 'AUS_VIE_stats.json'
        elif (matchOption == '1 February 2022 - Vietnam 3-1 China'):
            xgoalFile = 'VIE_CHN_xgoal_stats.json'
            eventsFile = 'VIE_CHN_events.json'
            statsFile = 'VIE_CHN_stats.json'
        elif (matchOption == '24 March 2022 - Vietnam 0-1 Oman'):
            xgoalFile = 'VIE_OMA_xgoal_stats.json'
            eventsFile = 'VIE_OMA_events.json'
            statsFile = 'VIE_OMA_stats.json'
        elif (matchOption == '29 March 2022 - Japan 1-1 Vietnam'):
            xgoalFile = 'JPN_VIE_xgoal_stats.json'
            eventsFile = 'JPN_VIE_events.json'
            statsFile = 'JPN_VIE_stats.json'

    elif (competitionOption == 'AFF Cup 2020'):
        directory = 'data/AFF Cup 2020/'

        if (matchOption == '6 December 2021 - Laos 0-2 Vietnam'):
            xgoalFile = 'LAO_VIE_xgoal_stats.json'
            eventsFile = 'LAO_VIE_events.json'
            statsFile = 'LAO_VIE_stats.json'
        elif (matchOption == '12 December 2021 - Vietnam 3-0 Malaysia'):
            xgoalFile = 'VIE_MAS_xgoal_stats.json'
            eventsFile = 'VIE_MAS_events.json'
            statsFile = 'VIE_MAS_stats.json'
        elif (matchOption == '15 December 2021 - Indonesia 0-0 Vietnam'):
            xgoalFile = 'IDN_VIE_xgoal_stats.json'
            eventsFile = 'IDN_VIE_events.json'
            statsFile = 'IDN_VIE_stats.json'
        elif (matchOption == '19 December 2021 - Vietnam 4-0 Cambodia'):
            xgoalFile = 'VIE_CAM_xgoal_stats.json'
            eventsFile = 'VIE_CAM_events.json'
            statsFile = 'VIE_CAM_stats.json'
        elif (matchOption == '23 December 2021 - Vietnam 0-2 Thailand'):
            xgoalFile = 'VIE_THA_xgoal_stats.json'
            eventsFile = 'VIE_THA_events.json'
            statsFile = 'VIE_THA_stats.json'
        elif (matchOption == '26 December 2021 - Thailand 0-0 Vietnam'):
            xgoalFile = 'THA_VIE_xgoal_stats.json'
            eventsFile = 'THA_VIE_events.json'
            statsFile = 'THA_VIE_stats.json'

    # Variables to store match and team's information
    matchName = ""
    compName = ""
    homeTeamId = ""
    awayTeamId = ""
    homeTeam = ""
    awayTeam = ""

    # Open the json file, copy its data, and then immediately close the json file
    with open(directory + statsFile, encoding='utf-8') as jsonFile:
        jsonData = json.load(jsonFile)
        jsonFile.close()

    # Create four lists to store players' info
    goalkeepers = pd.DataFrame()
    defenders = pd.DataFrame()
    midfielders = pd.DataFrame()
    attackers = pd.DataFrame()

    # Access the lineups file
    matchInfo = jsonData['matchInfo']
    liveData = jsonData['liveData']
    lineups = liveData['lineUp']

    # Gather necessary information
    matchName = matchInfo['description']
    compName = matchInfo['competition']['name']

    playerInfo = {
        'playerId': '',
        'playerName': '',
        'playingTime': 0
    }

    if (lineups[0]['contestantId'] == "a9rijkw11dvpb2ysf1pe3zcqo"):
        players = lineups[0]['player']
    elif (lineups[1]['contestantId'] == "a9rijkw11dvpb2ysf1pe3zcqo"):
        players = lineups[1]['player']

    for i in range(len(players)):

        isPlayed = False

        for stat in players[i]['stat']:

            if ("minsPlayed" == stat["type"]):
                minsPlayed = stat["value"]
                isPlayed = True

        if (isPlayed == True):

            playerId = players[i]['playerId']
            position = ''
            playerInfo['playerId'] = players[i]['playerId']
            playerInfo['playerName'] = players[i]['matchName']
            playerInfo['playingTime'] = minsPlayed

            if (players[i]['position'] != "Substitute"):
                position = players[i]['position']
            else:
                position = players[i]['subPosition']

            if (position == 'Goalkeeper'):

                if (len(goalkeepers) == 0):
                    goalkeepers = goalkeepers.append(
                        playerInfo, ignore_index=True)
                else:

                    for j in range(len(goalkeepers)):
                        isplayerinlist = False
                        if (playerId == goalkeepers['playerId'][j]):
                            isplayerinlist = True
                            break

                    if (isplayerinlist == False):
                        goalkeepers = goalkeepers.append(
                            playerInfo, ignore_index=True)

            elif (position == 'Defender') or (position == 'Wing Back'):

                if (len(defenders) == 0):
                    defenders = defenders.append(playerInfo, ignore_index=True)
                else:

                    for j in range(len(defenders)):
                        isplayerinlist = False
                        if (playerId == defenders['playerId'][j]):
                            isplayerinlist = True
                            break

                    if (isplayerinlist == False):
                        defenders = defenders.append(
                            playerInfo, ignore_index=True)

            elif (position == 'Midfielder'):

                if (len(midfielders) == 0):
                    midfielders = midfielders.append(
                        playerInfo, ignore_index=True)
                else:

                    for j in range(len(midfielders)):
                        isplayerinlist = False
                        if (playerId == midfielders['playerId'][j]):
                            isplayerinlist = True
                            break

                    if (isplayerinlist == False):
                        midfielders = midfielders.append(
                            playerInfo, ignore_index=True)

            elif (position == 'Attacker') or (position == 'Striker'):

                if (len(attackers) == 0):
                    attackers = attackers.append(playerInfo, ignore_index=True)
                else:

                    for j in range(len(attackers)):
                        isplayerinlist = False
                        if (playerId == attackers['playerId'][j]):
                            isplayerinlist = True
                            break

                    if (isplayerinlist == False):
                        attackers = attackers.append(
                            playerInfo, ignore_index=True)

    positionOption = st.radio(
        label="Choose player's position",
        options=("Goalkeeper",
                    "Defender",
                    "Midfielder",
                    "Attacker"
                    ),
        index=0
    )

    if (positionOption == 'Goalkeeper'):

        playerOption = st.selectbox(
            label='Players list',
            options=(goalkeepers['playerName'] +
                        ' - ' + goalkeepers['playingTime'] + ' mins played'),
            index=0
        )
    elif (positionOption == 'Defender'):

        playerOption = st.selectbox(
            label='Players list',
            options=(defenders['playerName'] + ' - ' +
                        defenders['playingTime'] + ' mins played'),
            index=0
        )
    elif (positionOption == 'Midfielder'):

        playerOption = st.selectbox(
            label='Players list',
            options=(midfielders['playerName'] + ' - ' +
                        midfielders['playingTime'] + ' mins played'),
            index=0
        )
    elif (positionOption == 'Attacker'):

        playerOption = st.selectbox(
            label='Players list',
            options=(attackers['playerName'] + ' - ' +
                        attackers['playingTime'] + ' mins played'),
            index=0
        )

# Split the chosen option to get the player's name
userOption = str(playerOption).split(" -")
idOption = ''  # Blank variable to store the chosen player's ID

# Find the chosen player's ID in the stats file
for i in range(len(players)):

    if (userOption[0] == players[i]['matchName']):
        idOption = players[i]['playerId']
        
# Import the fonts from the same folder as this code
robotoRegular = fm.FontProperties(fname='./Roboto-Regular.ttf')
robotoBold = fm.FontProperties(fname='./Roboto-Bold.ttf')

# Create two arrays with Opta's type IDs for the touch map
outfield_typeId = [1, 2, 3, 7, 8, 9, 12,
                    13, 14, 15, 16, 42, 44, 45, 50, 51, 61]
keeper_typeId = [1, 2, 3, 7, 8, 9, 10, 11, 12,
                    13, 14, 15, 16, 41, 42, 50, 52, 54, 61]

# Create blank variables to store touch data
touch_period = 0
touch_min = 0
touch_sec = 0
touch_type = 0
x_start = 0
y_start = 0

with col2:

    # Radio buttons to choose which visualisation to display
    vizOption = st.radio(
        label='Visualisation on display',
        options=("Touch map", "Individual actions"),
        index=0
    )

    # Detailed options for the visualisations
    if (vizOption == 'Touch map'):

        st.markdown('Touch map options')
        yesPasses = st.checkbox(
            label='Passes',
            value=True
        )
        yesDefActions = st.checkbox(
            label='Defensive actions',
            value=True
        )
        yesShots = st.checkbox(
            label='Shots',
            value=True
        )
        yesDribbles = st.checkbox(
            label='Dribbles',
            value=True
        )
        yesLostPos = st.checkbox(
            label='Lost possessions',
            value=True
        )

    elif (vizOption == 'Individual actions'):

        touchOption = st.radio(
            label='Individual actions options',
            options=("Shots",
                        "Passes",
                        "Crosses"),
            index=0
        )

# Open the json file, copy its data, and then immediately close the json file
with open(directory + eventsFile, encoding='utf-8') as jsonFile:
    jsonData = json.load(jsonFile)
    jsonFile.close()

liveData = jsonData['liveData']
event = liveData['event']

viz_info = ''

with st.spinner("Have a bite while you are waiting for this viz!"):

    if (vizOption == 'Touch map'):

        touches_data = []

        for touch in event:

            isqualifier = False

            if ("playerId" in touch) and (touch["playerId"] == idOption):

                if (touch["typeId"] in outfield_typeId):

                    for qualifier in touch['qualifier']:
                        if (qualifier['qualifierId'] == 123):
                            isqualifier = True
                            break

                    if (isqualifier == False):
                        touch_period = touch["periodId"]
                        touch_min = touch["timeMin"]
                        touch_sec = touch["timeSec"]
                        touch_type = touch["typeId"]

                        x_start = touch["x"]
                        y_start = touch["y"]

                        touch_outcome = touch["outcome"]

                        touches_data.append(
                            [touch_period, touch_min, touch_sec, touch_type, x_start, y_start, touch_outcome])

        # Set up and draw the pitch
        pitch = Pitch(positional=True, positional_color='white',
                        pitch_type='opta', pitch_color='#0e1117',
                        line_color="white", stripe=False, constrained_layout=True, tight_layout=True)
        fig, ax = pitch.draw(figsize=(10, 8))

        for i in range(len(touches_data)):

            if (yesPasses):
                if (touches_data[i][3] == 1) | (touches_data[i][3] == 2):
                    nodes = pitch.scatter(touches_data[i][4], touches_data[i][5], s=100, marker='o',
                                            color="cyan", edgecolors="cyan", zorder=1, ax=ax)

            if (yesDefActions):
                if (touches_data[i][3] == 7) | (touches_data[i][3] == 8) | (touches_data[i][3] == 12) | (touches_data[i][3] == 44) | (touches_data[i][3] == 45):
                    nodes = pitch.scatter(touches_data[i][4], touches_data[i][5], s=100, marker='o',
                                            color="green", edgecolors="green", zorder=1, ax=ax)

            if (yesShots):
                if (touches_data[i][3] == 13) | (touches_data[i][3] == 14) | (touches_data[i][3] == 15) | (touches_data[i][3] == 16):
                    nodes = pitch.scatter(touches_data[i][4], touches_data[i][5], s=100, marker='o',
                                            color="red", edgecolors="red", zorder=1, ax=ax)

            if (yesDribbles):
                if (touches_data[i][3] == 3) | (touches_data[i][3] == 42):
                    nodes = pitch.scatter(touches_data[i][4], touches_data[i][5], s=100, marker='o',
                                            color="yellow", edgecolors="yellow", zorder=1, ax=ax)

            if (yesLostPos):
                if (touches_data[i][3] == 9) | (touches_data[i][3] == 50) | (touches_data[i][3] == 51) | (touches_data[i][3] == 61):
                    nodes = pitch.scatter(touches_data[i][4], touches_data[i][5], s=100, marker='o',
                                            color="orange", edgecolors="orange", zorder=1, ax=ax)

            if (yesPasses and not yesDefActions and not yesShots and not yesDribbles and not yesLostPos):
                viz_info = userOption[0] + " | Passes"
            elif (yesDefActions and not yesPasses and not yesShots and not yesDribbles and not yesLostPos):
                viz_info = userOption[0] + " | Defensive actions"
            elif (yesShots and not yesPasses and not yesDefActions and not yesDribbles and not yesLostPos):
                viz_info = userOption[0] + " | Shots"
            elif (yesDribbles and not yesPasses and not yesDefActions and not yesShots and not yesLostPos):
                viz_info = userOption[0] + " | Dribbles"
            elif (yesLostPos and not yesPasses and not yesDefActions and not yesShots and not yesDribbles):
                viz_info = userOption[0] + " | Possessions lost"
            else:
                viz_info = userOption[0] + " | Touch map"

        ax.text(4, -3.5, 'Legend:', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(8.5, -2.5, s=100, marker='o',
                    color="cyan", edgecolors="cyan")
        ax.text(12, -3.5, 'Pass', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(15.5, -2.5, s=100, marker='o',
                    color="green", edgecolors="green")
        ax.text(23.5, -3.5, 'Defensive action', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(31.5, -2.5, s=100, marker='o',
                    color="red", edgecolors="red")
        ax.text(34.5, -3.5, 'Shot', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(37.5, -2.5, s=100, marker='o',
                    color="yellow", edgecolors="yellow")
        ax.text(41.5, -3.5, 'Dribble', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(45.5, -2.5, s=100, marker='o',
                    color="orange", edgecolors="orange")
        ax.text(53, -3.5, 'Possession lost', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')

        competition_info = matchName + " - " + compName

        ax.text(40 - (len(viz_info) / 2), 108, viz_info, color='white',
                fontproperties=robotoBold, fontsize=25, ha='left')
        ax.text(50 - (len(competition_info) / 2), 103, competition_info,
                color='white', fontproperties=robotoBold, fontsize=15, ha='left')
        ax.text(1, 97, "By Daryl - @dgouilard", color='white',
                fontproperties=robotoRegular, fontsize=9)

        ax.scatter(1, 102, s=200, marker="$→$",
                    color="white", edgecolors="white")
        ax.text(7.5, 101.5, 'Attacking direction', color='white',
                font_properties=robotoBold, fontsize=8, ha='center')

        fig.set_facecolor('#0e1117')
        fig.set_figwidth(10.5)
        fig.set_figheight(10)

    elif (vizOption == 'Individual actions') and (touchOption == 'Passes') or (vizOption == 'Individual actions') and (touchOption == 'Crosses'):

        starting_x = 0
        starting_y = 0
        ending_x = 0
        ending_y = 0

        passes_data = []

        for passes in event:

            isqualifier = False

            if ("playerId" in passes) and (passes["playerId"] == idOption):

                if (passes["typeId"] in [1, 2]):

                    isassist = 0
                    iskeypass = 0

                    if ("assist" in passes) and (passes["assist"] == 1):
                        isassist = 1

                    if ("keyPass" in passes) and (passes["keyPass"] == 1):
                        iskeypass = 1

                    if (touchOption == 'Crosses'):

                        for qualifier in passes["qualifier"]:

                            if (qualifier["qualifierId"] == 5) or (qualifier["qualifierId"] == 6):
                                break
                            else:
                                if (qualifier["qualifierId"] == 2):
                                    isqualifier = True

                                if (qualifier["qualifierId"] == 140):
                                    ending_x = float(qualifier["value"])

                                if (qualifier["qualifierId"] == 141):
                                    ending_y = float(qualifier["value"])

                        if (isqualifier == True):

                            passes_period = passes["periodId"]
                            passes_min = passes["timeMin"]
                            passes_sec = passes["timeSec"]
                            passes_outcome = passes["outcome"]

                            starting_x = passes["x"]
                            starting_y = passes["y"]

                            passes_data.append([passes_period, passes_min, passes_sec, passes_outcome,
                                                isassist, iskeypass, starting_x, starting_y, ending_x, ending_y])

                    elif (touchOption == 'Passes'):

                        for qualifier in passes["qualifier"]:

                            if (qualifier["qualifierId"] == 140):
                                ending_x = float(qualifier["value"])

                            if (qualifier["qualifierId"] == 141):
                                ending_y = float(qualifier["value"])

                        passes_period = passes["periodId"]
                        passes_min = passes["timeMin"]
                        passes_sec = passes["timeSec"]
                        passes_outcome = passes["outcome"]

                        starting_x = passes["x"]
                        starting_y = passes["y"]

                        passes_data.append([passes_period, passes_min, passes_sec, passes_outcome,
                                            isassist, iskeypass, starting_x, starting_y, ending_x, ending_y])

        # Set up and draw the pitch
        pitch = Pitch(positional=True, positional_color='white',
                        pitch_type='opta', pitch_color='#0e1117',
                        line_color="white", stripe=False, constrained_layout=True, tight_layout=True)
        fig, ax = pitch.draw(figsize=(10, 8))

        for i in range(len(passes_data)):

            if (passes_data[i][3] == 1):

                if (passes_data[i][4] == 1):
                    arrow = pitch.arrows(passes_data[i][6], passes_data[i][7], passes_data[i][8], passes_data[i]
                                            [9], width=1.5, headwidth=7, headaxislength=5, headlength=5, color='red', alpha=1, ax=ax)

                elif (passes_data[i][5] == 1):
                    arrow = pitch.arrows(passes_data[i][6], passes_data[i][7], passes_data[i][8], passes_data[i]
                                            [9], width=1.5, headwidth=7, headaxislength=5, headlength=5, color='yellow', alpha=1, ax=ax)

                else:
                    arrow = pitch.arrows(passes_data[i][6], passes_data[i][7], passes_data[i][8], passes_data[i]
                                            [9], width=1.5, headwidth=7, headaxislength=5, headlength=5, color='lime', alpha=1, ax=ax)

            else:
                arrow = pitch.arrows(passes_data[i][6], passes_data[i][7], passes_data[i][8], passes_data[i][9],
                                        width=1.5, headwidth=7, headaxislength=5, headlength=5, color='dodgerblue', alpha=1, ax=ax)

        if (touchOption == 'Passes'):
            viz_info = userOption[0] + ' | Passes'
        elif (touchOption == 'Crosses'):
            viz_info = userOption[0] + ' | Crosses'

        ax.text(4, -3.5, 'Legends:', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(10, -3, s=350, marker="$→$",
                    color="dodgerblue", edgecolors="dodgerblue")
        ax.text(17.5, -3.5, 'Unsuccessful', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(24.5, -3, s=350, marker="$→$",
                    color="lime", edgecolors="lime")
        ax.text(30.5, -3.5, 'Successful', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(36.5, -3, s=350, marker="$→$",
                    color="red", edgecolors="red")
        ax.text(41, -3.5, 'Assist', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')
        ax.scatter(45, -3, s=350, marker="$→$",
                    color="yellow", edgecolors="yellow")
        ax.text(50.5, -3.5, 'Key pass', color='white',
                font_properties=robotoBold, fontsize=12, ha='center')

        competition_info = matchName + " - " + compName

        ax.text(40 - (len(viz_info) / 2), 108, viz_info, color='white',
                fontproperties=robotoBold, fontsize=25, ha='left')
        ax.text(50 - (len(competition_info) / 2), 103, competition_info,
                color='white', fontproperties=robotoBold, fontsize=15, ha='left')
        ax.text(1, 97, "By Daryl - @dgouilard", color='white',
                fontproperties=robotoRegular, fontsize=9)

        ax.scatter(1, 102, s=200, marker="$→$",
                    color="white", edgecolors="white")
        ax.text(7.5, 101.5, 'Attacking direction', color='white',
                font_properties=robotoBold, fontsize=8, ha='center')

        fig.set_facecolor('#0e1117')
        fig.set_figwidth(10.5)
        fig.set_figheight(10)

    elif (vizOption == 'Individual actions') and (touchOption == 'Shots'):

        st.header(userOption[0] + ' | Shots')
        st.subheader(matchName + " - " + compName)

        with open(directory + xgoalFile, encoding='utf-8') as jsonFile:
            jsonData = json.load(jsonFile)
            jsonFile.close()

        liveData = jsonData['liveData']
        event = liveData['event']

        shots = []

        for shot in event:

            isqualifier = False

            if (shot['playerId'] == idOption):

                x_value = shot['x']
                y_value = shot['y']
                player_name = shot['playerName']

                for qualifier in shot['qualifier']:
                    if (qualifier['qualifierId'] == 321):
                        xg_value = float(qualifier['value'])

                    if (qualifier['qualifierId'] == 82):
                        isqualifier = True

                if (isqualifier == False):
                    shot_type = shot['typeId']
                else:
                    shot_type = 82

                shots.append(
                    [shot_type, x_value, y_value, xg_value, player_name])

        home_goals = 0
        home_on_target = 0
        blocked_shots = 0
        home_post = 0
        home_off_target = 0
        total_xg = 0

        pitch = VerticalPitch(pitch_type='opta', pitch_color='#0e1117',
                                line_color='white', constrained_layout=True, tight_layout=True, half=True)
        fig, ax = pitch.draw(figsize=(10, 8))

        teamColor = 'red'
        teamEdge = 'yellow'

        for i in range(0, len(shots)):

            if (shots[i][0] == 16):
                nodes = pitch.scatter(shots[i][1], shots[i][2], s=1500 * shots[i][3], marker='o',
                                        color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
                home_goals += 1
                home_on_target += 1
            elif (shots[i][0] == 15):
                nodes = pitch.scatter(shots[i][1], shots[i][2], s=1500 * shots[i][3], marker='^',
                                        color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
                home_on_target += 1
            elif (shots[i][0] == 82):
                nodes = pitch.scatter(shots[i][1], shots[i][2], s=1500 * shots[i][3], marker='D',
                                        color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
                blocked_shots += 1
            elif (shots[i][0] == 14):
                nodes = pitch.scatter(shots[i][1], shots[i][2], s=1500 * shots[i][3], marker='s',
                                        color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
                home_post += 1
            else:
                nodes = pitch.scatter(shots[i][1], shots[i][2], s=1500 * shots[i][3], marker='X',
                                        color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
                home_off_target += 1

            total_xg = total_xg + shots[i][3]

        teamColor = 'red'
        teamEdge = 'yellow'

        ax.text(99, 98.5, "By Daryl - @dgouilard", color='white',
                fontproperties=robotoRegular, fontsize=10)
        ax.text(98, 47.5, "Size of dot increases by the shot's xG value",
                color='white', fontproperties=robotoRegular, fontsize=10)

        text_box = dict(boxstyle='round', facecolor='white')
        home_values = dict(boxstyle='round', facecolor=teamColor,
                            edgecolor=teamEdge)

        ax.text(94, 65, 'Goals', color='black', font_properties=robotoBold,
                fontsize=12, ha='center', bbox=text_box)
        ax.text(79, 65, str(home_goals), color="white",
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)

        ax.text(90, 62, 'Shots on target', color='black',
                font_properties=robotoBold, fontsize=12, ha='center', bbox=text_box)
        ax.text(79, 62, str(home_on_target), color="white",
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)

        ax.text(90.5, 59, 'Shots blocked', color='black',
                font_properties=robotoBold, fontsize=12, ha='center', bbox=text_box)
        ax.text(79, 59, str(blocked_shots), color="white",
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)

        ax.text(93, 56, 'Hit post', color='black', font_properties=robotoBold,
                fontsize=12, ha='center', bbox=text_box)
        ax.text(79, 56, str(home_post), color="white",
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)

        ax.text(90, 53, 'Shots off target', color='black',
                font_properties=robotoBold, fontsize=12, ha='center', bbox=text_box)
        ax.text(79, 53, str(home_off_target), color="white",
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)

        ax.text(93, 50, 'Total xG', color='black', font_properties=robotoBold,
                fontsize=12, ha='center', bbox=text_box)
        ax.text(79, 50, str(round(total_xg, 2)), color="white",
                font_properties=robotoBold, fontsize=12, ha='left', bbox=home_values)

        ax.text(2, 63, 'Outcomes:', color='white',
                font_properties=robotoBold, fontsize=10, ha='right')
        nodes = pitch.scatter(61, 2, s=100, marker='o',
                                color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
        ax.text(5, 60.5, 'Goal', color='white',
                font_properties=robotoBold, fontsize=10, ha='center')
        nodes = pitch.scatter(58, 2, s=100, marker='^',
                                color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
        ax.text(6.5, 57.5, 'On target', color='white',
                font_properties=robotoBold, fontsize=10, ha='center')
        nodes = pitch.scatter(55, 2, s=100, marker='s',
                                color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
        ax.text(6.5, 54.5, 'Hit post', color='white',
                font_properties=robotoBold, fontsize=10, ha='center')
        nodes = pitch.scatter(52, 2, s=100, marker='D',
                                color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
        ax.text(6.5, 51.5, 'Blocked', color='white',
                font_properties=robotoBold, fontsize=10, ha='center')
        nodes = pitch.scatter(49, 2, s=100, marker='X',
                                color=teamColor, edgecolors=teamEdge, zorder=1, ax=ax)
        ax.text(6.8, 48.5, 'Off target', color='white',
                font_properties=robotoBold, fontsize=10, ha='center')

        fig.set_facecolor('#0e1117')

    # Ask Streamlit to plot the figure
    st.pyplot(fig)
