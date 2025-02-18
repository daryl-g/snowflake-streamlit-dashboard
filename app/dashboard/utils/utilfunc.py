# This file contains utility functions that are used in the dashboard.

# Necessary imports
import json
import base64
import streamlit as st
import matplotlib.font_manager as fm  # Import fonts

from typing import Tuple
from snowflake.snowpark import Session
from matplotlib import pyplot as plt


@st.cache_data
def get_app_name(_session: Session) -> str:
    return _session.sql("""
        select current_database()
    """).collect()[0]["CURRENT_DATABASE()"]


def render_image(filepath: str):
    """
    This function renders an image using Streamlit.

    :params str filepath: path to the image. Must have a valid file extension.
    """
    mime_type = filepath.split('.')[-1:][0].lower()
    with open(filepath, "rb") as f:
        content_bytes = f.read()
        content_b64encoded = base64.b64encode(content_bytes).decode()
        image_string = f'data:image/{mime_type};base64,{content_b64encoded}'
        st.image(image_string)

def save_and_render_figure(fig: plt.Figure, filepath: str = "plots/temp.png"):
    """
    This function saves a matplotlib figure object and renders it using Streamlit.

    :params plt.Figure fig: matplotlib figure object
    :params str filepath: path to save the figure. Must have a valid file extension. Default is "plots/temp.png"
    """
    fig.savefig(filepath, format="png", transparent=True)
    render_image(filepath)

def render_figure(fig: plt.Figure):
    """
    This function renders a matplotlib figure object using Streamlit.

    :params plt.Figure fig: matplotlib figure object
    """
    st.pyplot(fig)

# Function to open JSON files
def open_json(directory: str, file: str):
    """
    This function opens a JSON file and returns the data as a dictionary.

    :param str directory: The directory where the JSON file is located.
    :param str file: The name of the JSON file.
    """
    with open(directory + file, encoding='utf-8') as jsonFile:
        jsonData = json.load(jsonFile)
        jsonFile.close()

    return jsonData

def import_fonts() -> Tuple[fm.FontProperties, fm.FontProperties]:
    """
    This function imports the Roboto Regular and Roboto Bold fonts from the same folder as this code.

    :return: Tuple containing the Roboto Regular and Roboto Bold fonts.
    """
    # Import the fonts from the same folder as this code
    robotoRegular = fm.FontProperties(fname='./Roboto-Regular.ttf')
    robotoBold = fm.FontProperties(fname='./Roboto-Bold.ttf')

    return robotoRegular, robotoBold