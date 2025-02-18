# Import necessary libraries
import streamlit as st

from snowflake.snowpark import Session
from utils import render_image
from first_time_setup import render as render_first_time_setup, get_is_first_time_setup_dismissed

# Render function


def render(session: Session):

    menu_items = {
        "Get help": None,
        "Report a bug": None,
        "About": "Created by Daryl - @dgouilard."
    }

    st.set_page_config(
        page_title='Vietnam NT Data App',
        page_icon='🇻🇳',
        layout="wide",
        menu_items=menu_items
    )

    col1, col2 = st.columns([1.1, 5])

    with col1:
        render_image("Image.png")
    col2.title("Vietnam National Team Data App")

    st.header("Introduction")
    st.markdown(
        "The purpose of this application is to showcase the data of the Vietnam national football team\nthroughout the 2022 World Cup Asian Qualifiers campaign and the AFF Cup 2020 tournament."
    )
    st.markdown(
        "This is neither an official application from Opta (the data source for this app) nor the Vietnam Football Federation (VFF)."
    )
    st.markdown(
        "No profit or revenue are gained during the process of creating and maintaining this application."
    )
    st.markdown(
        "Reuse of the visualisations from this application is permitted.\nBut if you can credit the creator/link to the app to support my work, it would be greatly appreciated."
    )

    st.header("User guide")
    st.markdown(
        "-Navigate through the app using the widget on the left."
    )
    st.markdown(
        "-Choose **Player's data** for data and visualisations about players who have played in either or both competitions."
    )
    st.markdown(
        "-Choose **Match analysis** for data and visualisations from each of Vietnam's matches in both competitions."
    )
    st.subheader("How to save visualisation")
    st.markdown(
        "Just right click on the visualisation and choose 'Save image as', and you are done!"
    )
    st.subheader("Bug reporting")
    st.markdown(
        "To report a bug, you can send me a DM at @dgouilard on Twitter, or send me an email at daohoang.thai@gmail.com with the subject 'Data App Bug'. I will try to reply to you and log the bug as soon as I can."
    )

    st.header("Update log")
    st.markdown(
        "Will be updated whenever there is an update to the app."
    )

    st.subheader(
        "Created by Daryl Dao - @dgouilard\n(Vietnamese name: Đào Hoàng Thái, Twitter handle: @dgouilard)"
    )


if __name__ == "__main__":
    session = Session.builder.getOrCreate()
    session.custom_package_usage_config = {"enabled": True}

    if not get_is_first_time_setup_dismissed(session):
        render_first_time_setup(session)
    else:
        render(session)
