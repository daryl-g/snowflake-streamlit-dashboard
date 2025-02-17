# This file contains the code for the display data page.

# Necessary imports
import streamlit as st

from snowflake.snowpark import Session
from first_time_setup import get_is_first_time_setup_dismissed, render as render_first_time_setup