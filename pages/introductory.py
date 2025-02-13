import streamlit as st


def app():
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
    # st.markdown(
    #     "-Choose **Team's performance** for data and visualisations about Vietnam's national team."
    # )
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
