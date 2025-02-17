import streamlit as st
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm
from mplsoccer import Pitch, VerticalPitch
mpl.rcParams['figure.dpi'] = 300

# Page setup

# Page title
st.title("Player's overall data")

wcDirectory = 'data/2022 World Cup Asian Qualifiers/'
affDirectory = 'data/AFF Cup 2020/'

wcStatsList = ['AUS_VIE_stats.json', 'CHN_VIE_stats.json',
               'JPN_VIE_stats.json', 'KSA_VIE_stats.json',
               'OMA_VIE_stats.json', 'VIE_AUS_stats.json',
               'VIE_CHN_stats.json', 'VIE_JPN_stats.json',
               'VIE_KSA_stats.json', 'VIE_OMA_stats.json']

wcEventsList = ['AUS_VIE_events.json', 'CHN_VIE_events.json',
                'JPN_VIE_events.json', 'KSA_VIE_events.json',
                'OMA_VIE_events.json', 'VIE_AUS_events.json',
                'VIE_CHN_events.json', 'VIE_JPN_events.json',
                'VIE_KSA_events.json', 'VIE_OMA_events.json']

wcXGoalsList = ['AUS_VIE_xgoal_stats.json', 'CHN_VIE_xgoal.json',
                'JPN_VIE_xgoal_stats.json', 'KSA_VIE_xgoal.json',
                'OMA_VIE_xgoal_stats.json', 'VIE_AUS_xgoal.json',
                'VIE_CHN_xgoal_stats.json', 'VIE_JPN_xgoal_stats.json',
                'VIE_KSA_xgoal_stats.json', 'VIE_OMA_xgoal_stats.json']

affStatsList = ['IDN_VIE_stats.json', 'LAO_VIE_stats.json',
                'THA_VIE_stats.json', 'VIE_CAM_stats.json',
                'VIE_MAS_stats.json', 'VIE_THA_stats.json']

affEventsList = ['IDN_VIE_events.json', 'LAO_VIE_events.json',
                 'THA_VIE_events.json', 'VIE_CAM_events.json',
                 'VIE_MAS_events.json', 'VIE_THA_events.json']

affXGoalsList = ['IDN_VIE_xgoal_stats.json', 'LAO_VIE_xgoal_stats.json',
                 'THA_VIE_xgoal_stats.json', 'VIE_CAM_xgoal_stats.json',
                 'VIE_MAS_xgoal_stats.json', 'VIE_THA_xgoal_stats.json']

# Import the fonts from the same folder as this code
robotoRegular = fm.FontProperties(fname='./Roboto-Regular.ttf')
robotoBold = fm.FontProperties(fname='./Roboto-Bold.ttf')


def playersListExtractor(directory1, files_list1, directory2, files_list2, chosenPosition):

    playersList = pd.DataFrame()

    for file1 in files_list1:

        with open(directory1 + file1, encoding='utf-8') as jsonFile:
            jsonData = json.load(jsonFile)
            jsonFile.close()

        liveData = jsonData['liveData']
        lineups = liveData['lineUp']

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
                    minsPlayed = int(stat["value"])
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

                if (playerId == '93fvqt16qfegqs2e9lp6yduc5') and (position == 'Midfielder'):
                    position = 'Defender'
                elif (playerId == 'dcs7trihxgq30h0972bqfd815') and (position == 'Midfielder'):
                    position = 'Defender'
                elif (playerId == '5od5sv60o869jbzsgsdh16eol') and (position == 'Midfielder'):
                    position = 'Defender'
                elif (playerId == '4qe9v3ndhrzjm7aar3j78bkkp') and (position == 'Midfielder'):
                    position = 'Defender'
                elif (playerId == '9jm943d39ny1s8w0qlkmpk0ve') and (position == 'Midfielder'):
                    position = 'Defender'
                elif (playerId == '77ipvasiwsyshd44tly4iue39') and ((position == 'Striker') or (position == 'Attacker')):
                    position = 'Midfielder'
                elif (playerId == '88ncgjvhuhvowy5x9zzd2d5ud') and ((position == 'Striker') or (position == 'Attacker')):
                    position = 'Midfielder'

                for k in range(len(chosenPosition)):

                    if (position == chosenPosition[k]):

                        if (len(playersList) == 0):
                            playersList = pd.concat([playersList, pd.DataFrame(playerInfo, index=[0])], ignore_index=True)
                        else:

                            for j in range(len(playersList)):
                                isplayerinlist = False
                                if (playerId == playersList['playerId'][j]):
                                    playersList['playingTime'][j] = int(
                                        playersList['playingTime'][j]) + int(minsPlayed)
                                    isplayerinlist = True
                                    break

                            if (isplayerinlist == False):
                                playersList = pd.concat([playersList, pd.DataFrame(playerInfo, index=[0])], ignore_index=True)

    if (directory2 != '') and (files_list2 != ''):

        for file2 in files_list2:

            with open(directory2 + file2, encoding='utf-8') as jsonFile:
                jsonData = json.load(jsonFile)
                jsonFile.close()

            liveData = jsonData['liveData']
            lineups = liveData['lineUp']

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
                        minsPlayed = int(stat["value"])
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

                    if (playerId == '93fvqt16qfegqs2e9lp6yduc5') and (position == 'Midfielder'):
                        position = 'Defender'
                    elif (playerId == 'dcs7trihxgq30h0972bqfd815') and (position == 'Midfielder'):
                        position = 'Defender'
                    elif (playerId == '5od5sv60o869jbzsgsdh16eol') and (position == 'Midfielder'):
                        position = 'Defender'
                    elif (playerId == '4qe9v3ndhrzjm7aar3j78bkkp') and (position == 'Midfielder'):
                        position = 'Defender'
                    elif (playerId == '9jm943d39ny1s8w0qlkmpk0ve') and (position == 'Midfielder'):
                        position = 'Defender'
                    elif (playerId == '77ipvasiwsyshd44tly4iue39') and ((position == 'Striker') or (position == 'Attacker')):
                        position = 'Midfielder'
                    elif (playerId == '88ncgjvhuhvowy5x9zzd2d5ud') and ((position == 'Striker') or (position == 'Attacker')):
                        position = 'Midfielder'

                    for k in range(len(chosenPosition)):

                        if (position == chosenPosition[k]):

                            if (len(playersList) == 0):
                                playersList = pd.concat([playersList, pd.DataFrame(playerInfo, index=[0])], ignore_index=True)
                            else:

                                for j in range(len(playersList)):
                                    isplayerinlist = False
                                    if (playerId == playersList['playerId'][j]):
                                        playersList['playingTime'][j] = int(
                                            playersList['playingTime'][j]) + int(minsPlayed)
                                        isplayerinlist = True
                                        break

                                if (isplayerinlist == False):
                                    playersList = pd.concat([playersList, pd.DataFrame(playerInfo, index=[0])], ignore_index=True)

        return playersList
    else:
        return playersList


col1, col2 = st.columns(2)

with col1:

    # Select box to choose competition
    competitionOption = st.radio(
        label='Choose competition',
        options=('2022 World Cup Asian Qualifiers',
                 'AFF Cup 2020',
                 'All competitions'),
        index=0
    )

    # Buttons to select player's position
    positionOption = st.radio(
        label="Choose player's position",
        options=('Goalkeeper',
                 'Defender',
                 'Midfielder',
                 'Attacker'),
        index=0
    )

    goalkeepers = pd.DataFrame()
    defenders = pd.DataFrame()
    midfielders = pd.DataFrame()
    attackers = pd.DataFrame()

    if (competitionOption == '2022 World Cup Asian Qualifiers'):

        goalkeepers = playersListExtractor(
            wcDirectory, wcStatsList, '', '', ['Goalkeeper'])
        defenders = playersListExtractor(wcDirectory, wcStatsList, '', '', [
            'Defender', 'Wing Back'])
        midfielders = playersListExtractor(
            wcDirectory, wcStatsList, '', '', ['Midfielder'])
        attackers = playersListExtractor(
            wcDirectory, wcStatsList, '', '', ['Striker', 'Attacker'])

    elif (competitionOption == 'AFF Cup 2020'):

        goalkeepers = playersListExtractor(
            affDirectory, affStatsList, '', '', ['Goalkeeper'])
        defenders = playersListExtractor(affDirectory, affStatsList, '', '', [
            'Defender', 'Wing Back'])
        midfielders = playersListExtractor(
            affDirectory, affStatsList, '', '', ['Midfielder'])
        attackers = playersListExtractor(
            affDirectory, affStatsList, '', '', ['Striker', 'Attacker'])

    elif (competitionOption == 'All competitions'):

        goalkeepers = playersListExtractor(
            wcDirectory, wcStatsList, affDirectory, affStatsList, ['Goalkeeper'])
        defenders = playersListExtractor(
            wcDirectory, wcStatsList, affDirectory, affStatsList, ['Defender', 'Wing Back'])
        midfielders = playersListExtractor(
            wcDirectory, wcStatsList, affDirectory, affStatsList, ['Midfielder'])
        attackers = playersListExtractor(
            wcDirectory, wcStatsList, affDirectory, affStatsList, ['Striker', 'Attacker'])

    if (positionOption == 'Goalkeeper'):

        playerOption = st.selectbox(
            label='Players list',
            options=(goalkeepers['playerName']),
            index=0
        )
    elif (positionOption == 'Defender'):

        playerOption = st.selectbox(
            label='Players list',
            options=(defenders['playerName']),
            index=0
        )

    elif (positionOption == 'Midfielder'):

        playerOption = st.selectbox(
            label='Players list',
            options=(midfielders['playerName']),
            index=0
        )

    elif (positionOption == 'Attacker'):

        playerOption = st.selectbox(
            label='Players list',
            options=(attackers['playerName']),
            index=0
        )

# Split the chosen option to get the player's name
userOption = str(playerOption).split(" -")
idOption = ''  # Blank variable to store the chosen player's ID

# Find the chosen player's ID in the stats file
if (positionOption == 'Goalkeeper'):

    for i in range(len(goalkeepers)):

        if (userOption[0] == goalkeepers['playerName'][i]):
            idOption = goalkeepers['playerId'][i]

elif (positionOption == 'Defender'):

    for i in range(len(defenders)):

        if (userOption[0] == defenders['playerName'][i]):
            idOption = defenders['playerId'][i]

elif (positionOption == 'Midfielder'):

    for i in range(len(midfielders)):

        if (userOption[0] == midfielders['playerName'][i]):
            idOption = midfielders['playerId'][i]

elif (positionOption == 'Attacker'):

    for i in range(len(attackers)):

        if (userOption[0] == attackers['playerName'][i]):
            idOption = attackers['playerId'][i]

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

with st.spinner("The app is trying its hardest to bring you the best viz!"):

    viz_info = ''

    if (vizOption == 'Touch map'):

        touches_data = []

        if (competitionOption == '2022 World Cup Asian Qualifiers'):

            competition_info = competitionOption

            for eventsFile in wcEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(wcDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

        elif (competitionOption == 'AFF Cup 2020'):

            competition_info = competitionOption

            for eventsFile in affEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(affDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

        elif (competitionOption == 'All competitions'):

            competition_info = '2022 Asian Qualifiers & AFF Cup 2020'

            for eventsFile in wcEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(wcDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

            for eventsFile in affEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(affDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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
                      line_color="white", stripe=False)
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

        if (competitionOption == '2022 World Cup Asian Qualifiers'):

            competition_info = competitionOption

            for eventsFile in wcEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(wcDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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
                                            ending_x = float(
                                                qualifier["value"])

                                        if (qualifier["qualifierId"] == 141):
                                            ending_y = float(
                                                qualifier["value"])

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
                                        ending_x = float(
                                            qualifier["value"])

                                    if (qualifier["qualifierId"] == 141):
                                        ending_y = float(
                                            qualifier["value"])

                                passes_period = passes["periodId"]
                                passes_min = passes["timeMin"]
                                passes_sec = passes["timeSec"]
                                passes_outcome = passes["outcome"]

                                starting_x = passes["x"]
                                starting_y = passes["y"]

                                passes_data.append([passes_period, passes_min, passes_sec, passes_outcome,
                                                    isassist, iskeypass, starting_x, starting_y, ending_x, ending_y])

        elif (competitionOption == 'AFF Cup 2020'):

            competition_info = competitionOption

            for eventsFile in affEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(affDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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
                                            ending_x = float(
                                                qualifier["value"])

                                        if (qualifier["qualifierId"] == 141):
                                            ending_y = float(
                                                qualifier["value"])

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
                                        ending_x = float(
                                            qualifier["value"])

                                    if (qualifier["qualifierId"] == 141):
                                        ending_y = float(
                                            qualifier["value"])

                                passes_period = passes["periodId"]
                                passes_min = passes["timeMin"]
                                passes_sec = passes["timeSec"]
                                passes_outcome = passes["outcome"]

                                starting_x = passes["x"]
                                starting_y = passes["y"]

                                passes_data.append([passes_period, passes_min, passes_sec, passes_outcome,
                                                    isassist, iskeypass, starting_x, starting_y, ending_x, ending_y])

        elif (competitionOption == 'All competitions'):

            competition_info = '2022 Asian Qualifiers & AFF Cup 2020'

            for eventsFile in wcEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(wcDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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
                                            ending_x = float(
                                                qualifier["value"])

                                        if (qualifier["qualifierId"] == 141):
                                            ending_y = float(
                                                qualifier["value"])

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
                                        ending_x = float(
                                            qualifier["value"])

                                    if (qualifier["qualifierId"] == 141):
                                        ending_y = float(
                                            qualifier["value"])

                                passes_period = passes["periodId"]
                                passes_min = passes["timeMin"]
                                passes_sec = passes["timeSec"]
                                passes_outcome = passes["outcome"]

                                starting_x = passes["x"]
                                starting_y = passes["y"]

                                passes_data.append([passes_period, passes_min, passes_sec, passes_outcome,
                                                    isassist, iskeypass, starting_x, starting_y, ending_x, ending_y])

            for eventsFile in affEventsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(affDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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
                                            ending_x = float(
                                                qualifier["value"])

                                        if (qualifier["qualifierId"] == 141):
                                            ending_y = float(
                                                qualifier["value"])

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
                                        ending_x = float(
                                            qualifier["value"])

                                    if (qualifier["qualifierId"] == 141):
                                        ending_y = float(
                                            qualifier["value"])

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
                      line_color="white", stripe=False)
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

        shots = []

        if (competitionOption == '2022 World Cup Asian Qualifiers'):

            competition_info = competitionOption

            for eventsFile in wcXGoalsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(wcDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

        elif (competitionOption == 'AFF Cup 2020'):

            competition_info = competitionOption

            for eventsFile in affXGoalsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(affDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

        elif (competitionOption == 'All competitions'):

            competition_info = '2022 Asian Qualifiers & AFF Cup 2020'

            for eventsFile in wcXGoalsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(wcDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

            for eventsFile in affXGoalsList:

                # Open the json file, copy its data, and then immediately close the json file
                with open(affDirectory + eventsFile, encoding='utf-8') as jsonFile:
                    jsonData = json.load(jsonFile)
                    jsonFile.close()

                liveData = jsonData['liveData']
                event = liveData['event']

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

        st.header(userOption[0] + ' | Shots')
        st.subheader(competition_info)

        home_goals = 0
        home_on_target = 0
        blocked_shots = 0
        home_post = 0
        home_off_target = 0
        total_xg = 0

        pitch = VerticalPitch(pitch_type='opta', pitch_color='#0e1117',
                              line_color='white', half=True)
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
