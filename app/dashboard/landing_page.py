# Import necessary libraries
import streamlit as st
from PIL import Image
from pages.MultiPage import MultiPage
from pages import introductory, how_to, player_overall, player_individual, matches_lastmatch

menu_items = {
    "Get help": None,
    "Report a bug": None,
    "About": "Created by Daryl - @dgouilard on Twitter."
}

st.set_page_config(
    page_title='Vietnam NT Data App',
    page_icon='🇻🇳',
    layout="wide",
    menu_items = menu_items
)

app = MultiPage()

col1, col2 = st.columns([1.1, 5])
image = Image.open('Image.png')

col1.image(image, width=150, output_format='PNG')
col2.title("Vietnam National Team Data App")

app.add_page("Introduction", introductory.app)
app.add_page("How to read football vizzes", how_to.app)
# app.add_page("Team's performance", team_performance.app)
app.add_page("Player's overall data", player_overall.app)
app.add_page("Player's competition data", player_individual.app)
app.add_page("Match general analysis", matches_lastmatch.app)
# app.add_page("Match detailed analysis", matches_detailed.app)

app.run()
