# This file contains the code for the page that displays the visualisations for a selected match.

# Necessary imports
import streamlit as st  # Main library to create the web app
import matplotlib as mpl  # Increase quality of the visualisation
import matplotlib.pyplot as plt # Plotting library

from snowflake.snowpark import Session
from first_time_setup import render as render_first_time_setup, get_is_first_time_setup_dismissed
# Import from utilsfunc
from utils import save_and_render_figure
# Import from datafunc
from utils import dataFunc
# Import plot classes
from utils import xGTimeline, shotMap, passNetwork

mpl.rcParams['figure.dpi'] = 300

# Page setup

def render(session: Session):

    # Page title
    st.title("Match data analysis")

    # Select box to choose competition
    competitionOption = st.radio(
        label='Choose competition',
        options=('2022 World Cup Asian Qualifiers', 'AFF Cup 2020'),
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

    # Radio buttons to choose which visualisation to display
    vizOption = st.radio(
        label='Visualisation on display',
        options=('xG timeline', 'Shot map', "Home team passing network",
                "Away team passing network"),
        index=0
    )

    # Data processing:
    #
    # Goals:
    # -Create a dataset to use for both the xG timeline and the shot map/use for both passing networks
    # -Dataset used for the xG timeline and the shot map needs the length of each half
    # to calculate the displaying minutes (use events file with typeId 30)
    # -Limit the attempts to process the data and open the json files

    # Variables to store match and team's information
    matchName = ""
    compName = ""
    homeTeam = ""
    awayTeam = ""

    # Assign json files that belong to the chosen match
    xgoalFile = ''
    passnetworkFile = ''

    if (competitionOption == '2022 World Cup Asian Qualifiers'):
        directory = 'data/2022 World Cup Asian Qualifiers/'

        if (matchOption == '3 September 2021 - Saudi Arabia 3-1 Vietnam'):
            xgoalFile = 'KSA_VIE_xgoal.json'
            passnetworkFile = 'KSA_VIE_pass.json'
            eventsFile = 'KSA_VIE_events.json'
        elif (matchOption == '7 September 2021 - Vietnam 0-1 Australia'):
            xgoalFile = 'VIE_AUS_xgoal.json'
            passnetworkFile = 'VIE_AUS_pass_matrix.json'
            eventsFile = 'VIE_AUS_events.json'
        elif (matchOption == '8 October 2021 - China 3-2 Vietnam'):
            xgoalFile = 'CHN_VIE_xgoal.json'
            passnetworkFile = 'CHN_VIE_pass_matrix.json'
            eventsFile = 'CHN_VIE_events.json'
        elif (matchOption == '13 October 2021 - Oman 3-1 Vietnam'):
            xgoalFile = 'OMA_VIE_xgoal_stats.json'
            passnetworkFile = 'OMA_VIE_pass_matrix.json'
            eventsFile = 'OMA_VIE_events.json'
        elif (matchOption == '11 November 2021 - Vietnam 0-1 Japan'):
            xgoalFile = 'VIE_JPN_xgoal_stats.json'
            passnetworkFile = 'VIE_JPN_pass_matrix.json'
            eventsFile = 'VIE_JPN_events.json'
        elif (matchOption == '16 November 2021 - Vietnam 0-1 Saudi Arabia'):
            xgoalFile = 'VIE_KSA_xgoal_stats.json'
            passnetworkFile = 'VIE_KSA_pass_matrix.json'
            eventsFile = 'VIE_KSA_events.json'
        elif (matchOption == '27 January 2022 - Australia 4-0 Vietnam'):
            xgoalFile = 'AUS_VIE_xgoal_stats.json'
            passnetworkFile = 'AUS_VIE_pass_matrix.json'
            eventsFile = 'AUS_VIE_events.json'
        elif (matchOption == '1 February 2022 - Vietnam 3-1 China'):
            xgoalFile = 'VIE_CHN_xgoal_stats.json'
            passnetworkFile = 'VIE_CHN_pass_matrix.json'
            eventsFile = 'VIE_CHN_events.json'
        elif (matchOption == '24 March 2022 - Vietnam 0-1 Oman'):
            xgoalFile = 'VIE_OMA_xgoal_stats.json'
            passnetworkFile = 'VIE_OMA_pass_matrix.json'
            eventsFile = 'VIE_OMA_events.json'
        elif (matchOption == '29 March 2022 - Japan 1-1 Vietnam'):
            xgoalFile = 'JPN_VIE_xgoal_stats.json'
            passnetworkFile = 'JPN_VIE_pass_matrix.json'
            eventsFile = 'JPN_VIE_events.json'
        elif (matchOption == '29 March 2022 - Japan 1-1 Vietnam'):
            xgoalFile = 'JPN_VIE_xgoal_stats.json'
            passnetworkFile = 'JPN_VIE_pass_matrix.json'
            eventsFile = 'JPN_VIE_events.json'

    elif (competitionOption == 'AFF Cup 2020'):
        directory = 'data/AFF Cup 2020/'

        if (matchOption == '6 December 2021 - Laos 0-2 Vietnam'):
            xgoalFile = 'LAO_VIE_xgoal_stats.json'
            passnetworkFile = 'LAO_VIE_pass_matrix.json'
            eventsFile = 'LAO_VIE_events.json'
        elif (matchOption == '12 December 2021 - Vietnam 3-0 Malaysia'):
            xgoalFile = 'VIE_MAS_xgoal_stats.json'
            passnetworkFile = 'VIE_MAS_pass_matrix.json'
            eventsFile = 'VIE_MAS_events.json'
        elif (matchOption == '15 December 2021 - Indonesia 0-0 Vietnam'):
            xgoalFile = 'IDN_VIE_xgoal_stats.json'
            passnetworkFile = 'IDN_VIE_pass_matrix.json'
            eventsFile = 'IDN_VIE_events.json'
        elif (matchOption == '19 December 2021 - Vietnam 4-0 Cambodia'):
            xgoalFile = 'VIE_CAM_xgoal_stats.json'
            passnetworkFile = 'VIE_CAM_pass_matrix.json'
            eventsFile = 'VIE_CAM_events.json'
        elif (matchOption == '23 December 2021 - Vietnam 0-2 Thailand'):
            xgoalFile = 'VIE_THA_xgoal_stats.json'
            passnetworkFile = 'VIE_THA_pass_matrix.json'
            eventsFile = 'VIE_THA_events.json'
        elif (matchOption == '26 December 2021 - Thailand 0-0 Vietnam'):
            xgoalFile = 'THA_VIE_xgoal_stats.json'
            passnetworkFile = 'THA_VIE_pass_matrix.json'
            eventsFile = 'THA_VIE_events.json'

    # Create an instance of the plot classes
    xG_timeline = xGTimeline(directory, eventsFile, xgoalFile)
    shot_map = shotMap(directory, eventsFile, xgoalFile)
    pass_network = passNetwork(directory, passnetworkFile)

    # A reminder to stay hydrated while the program is working!
    with st.spinner("While waiting, remember to stay hydrated!"):

        # Create a dataFunc object
        events_funcs = dataFunc(directory, eventsFile)

        matchName = events_funcs.get_match_name()
        compName = events_funcs.get_competition_name()

        # Set the page header to the match's information
        st.header(matchName + ' - ' + compName)

        # Get the necessary information about both teams
        homeTeamId, homeTeam, awayTeamId, awayTeam = events_funcs.get_team_info()

        if (homeTeam == 'Vietnam'):
            home_colour = 'red'
            home_edge_colour = 'yellow'

            if (awayTeam == 'Australia'):
                away_colour = '#ffcd00'
                away_edge_colour = '#00843d'
            elif (awayTeam == 'Saudi Arabia'):
                away_colour = '#006c35'
                away_edge_colour = 'white'
            elif (awayTeam == 'China PR'):
                away_colour = '#cd101e'
                away_edge_colour = '#f2d972'
            elif (awayTeam == 'Oman'):
                away_colour = 'green'
                away_edge_colour = 'red'
            else:
                away_colour = 'darkblue'
                away_edge_colour = 'white'

        else:
            away_colour = 'red'
            away_edge_colour = 'yellow'

            if (homeTeam == 'Australia'):
                home_colour = '#ffcd00'
                home_edge_colour = '#00843d'
            elif (homeTeam == 'Saudi Arabia'):
                home_colour = '#006c35'
                home_edge_colour = 'white'
            elif (homeTeam == 'China PR'):
                home_colour = '#cd101e'
                home_edge_colour = '#f2d972'
            elif (homeTeam == 'Oman'):
                home_colour = 'green'
                home_edge_colour = 'red'
            else:
                home_colour = 'darkblue'
                home_edge_colour = 'white'

        # If the chosen option is either xG timeline or shot map
        if (vizOption == 'xG timeline'):

            fig: plt.Figure = xG_timeline.plot_xG_timeline(
                home_colour,
                away_colour,
                home_edge_colour,
                away_edge_colour,
            )

        elif (vizOption == 'Shot map'):

            fig: plt.Figure = shot_map.plot_shot_map(
                home_colour,
                away_colour,
                home_edge_colour,
                away_edge_colour,
            )

        # If the chosen option is either home team's passing network or away team's passing network
        elif (vizOption == "Home team passing network"):

            fig: plt.Figure = pass_network.plot_pass_network(
                home_colour,
                home_edge_colour,
                which_team = "home"
            )

        elif (vizOption == "Away team passing network"):

            fig: plt.Figure = pass_network.plot_pass_network(
                away_colour,
                away_edge_colour,
                which_team = "away"
            )

        # Ask Streamlit to plot the figure
        ## Paths to save figures
        figure_path = "plots/"
        match_name = eventsFile.split("_")[0] + "_" + eventsFile.split("_")[1]
        figure_name = match_name + "_" + vizOption.replace(" ", "_").lower() + ".png"

        save_and_render_figure(
            fig=fig,
            filepath=figure_path + figure_name
        )

if __name__ == "__main__":
    session = Session.builder.getOrCreate()
    if not get_is_first_time_setup_dismissed(session):
        render_first_time_setup(session)
    else:
        render(session)
