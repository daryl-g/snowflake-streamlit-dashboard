# This file contains utility functions that are used in the dashboard.

import base64
import streamlit as st

from snowflake.snowpark import Session
from matplotlib import pyplot as plt


@st.cache_data
def get_app_name(_session: Session) -> str:
    return _session.sql("""
        select current_database()
    """).collect()[0]["CURRENT_DATABASE()"]


def render_image(filepath: str):
    """
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
    :params plt.Figure fig: matplotlib figure object

    :params str filepath: path to save the figure. Must have a valid file extension. Default is "plots/temp.png"
    """
    fig.savefig(filepath, format="png", transparent=True)
    render_image(filepath)

def render_figure(fig: plt.Figure):
    """
    :params plt.Figure fig: matplotlib figure object
    """
    st.pyplot(fig)