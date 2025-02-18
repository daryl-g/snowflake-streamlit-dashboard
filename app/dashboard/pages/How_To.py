# This file contains the code to render the instructions page of the app.

# Necessary imports
import streamlit as st
import matplotlib as mpl  # Increase quality of the visualisation
import matplotlib.pyplot as plt  # Draw the xG timeline

from snowflake.snowpark import Session
from first_time_setup import render as render_first_time_setup, get_is_first_time_setup_dismissed

# Imports from utilfunc
from utils import save_and_render_figure, import_fonts
# Imports from xG_timeline
from utils import xGTimeline, shotMap, passNetwork

mpl.rcParams['figure.dpi'] = 300

# Global variables
directory = 'data/2022 World Cup Asian Qualifiers/'
xgoalFile = 'JPN_VIE_xgoal_stats.json'
eventsFile = 'JPN_VIE_events.json'
passnetworkFile = 'JPN_VIE_pass_matrix.json'

# Get the fonts
robotoRegular, robotoBold = import_fonts()

# Create an instance of the xG_timeline class
xG_timeline = xGTimeline(directory, eventsFile, xgoalFile)
# Create an instance of the shotMap class
shot_map = shotMap(directory, eventsFile, xgoalFile)
# Create an instance of the passNetwork class
passing_network = passNetwork(directory, passnetworkFile)

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

    # Paths to save figures
    figure_path = "plots/"
    match_name = eventsFile.split("_")[0] + "_" + eventsFile.split("_")[1]

    # A wish to the user while they are waiting for the viz
    with st.spinner("Hope you are having a good day! These instructions will be with you shortly."):

        if (userOption == 'xG timeline'):

            # Create the xG timeline
            fig: plt.Figure = xG_timeline.plot_xG_timeline(
                home_colour = 'darkblue',
                home_edge_colour = 'white',
                away_colour = 'red',
                away_edge_colour = 'yellow',
            )
            save_and_render_figure(
                fig=fig,
                filepath=figure_path + match_name + "_xG_timeline.png",
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
            fig: plt.Figure = shot_map.plot_shot_map(
                home_colour = 'darkblue',
                home_edge_colour = 'white',
                away_colour = 'red',
                away_edge_colour = 'yellow',
            )
            save_and_render_figure(
                fig=fig,
                filepath=figure_path + match_name + "_shot_map.png",
            )

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
            fig: plt.Figure = passing_network.plot_pass_network(
                team_colour = 'red',
                team_edge_colour = 'yellow',
                which_team = 'away',
            )
            save_and_render_figure(
                fig=fig,
                filepath=figure_path + match_name + "_passing_network.png",
            )

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
