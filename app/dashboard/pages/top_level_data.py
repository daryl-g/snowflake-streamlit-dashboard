# This file contains the code for the display data page.

# Necessary imports
import streamlit as st
import pandas as pd

from snowflake.snowpark import Session
from first_time_setup import get_is_first_time_setup_dismissed, render as render_first_time_setup

# Function to get data from Snowflake


@st.cache_data
def get_data(_session: Session, table_name: str) -> pd.DataFrame:
    modified_table_name: str = table_name.upper().replace(" ", "_")
    # Query to get data from Snowflake
    query = f"select * from reference('{modified_table_name}') as {modified_table_name}"
    return session.sql(query).to_pandas()

# Function to render the page


def render(session: Session):
    # Title of the page
    st.title("View raw Opta data")

    # Dropdown to select the table
    table_name = st.selectbox("Available tables", [
                              "Contestants", "Competitions", "Matches Info", "Match Details"])

    # Get data from Snowflake
    data: pd.DataFrame = get_data(session, table_name)

    # Display the data
    st.dataframe(data, use_container_width=True)

    # Option to download the data
    st.download_button(
        label="Download data as csv",
        data=data.to_csv(index=False, encoding="utf-8", sep=","),
        file_name=f"opta_{table_name}.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    session = Session.builder.getOrCreate()
    if not get_is_first_time_setup_dismissed(session):
        render_first_time_setup(session)
    else:
        render(session)
