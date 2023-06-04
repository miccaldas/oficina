"""
Module Docstring
"""
import json

import numpy as np
import pandas as pd
import snoop
import streamlit as st
from mysql.connector import Error, connect
from snoop import pp
from streamlit_timeline import st_timeline


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def db_items():
    """
    Collects data from the db.
    """
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes",
            use_pure=True,
        )
        cur = conn.cursor(buffered=True)
        # In order to use the 'groups' function is vis.js, the items dictionaries must have a 'group' key.
        # MySQL doesn't let me call a column 'group', So we'll call it something else and change it after.
        query = "SELECT title, tags AS content, string_date AS start FROM tags_streamlit"
        timedata = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return timedata


# @snoop
def dataframe_to_dict():
    """
    Converts dataframe to dictionary
    """
    td = db_items()
    tdict = td.to_dict("records")

    return tdict


@snoop
def vis_timeline():
    """"""
    st.set_page_config(layout="wide")

    dfs = dataframe_to_dict()

    timeline = st_timeline(dfs, groups=[], options={}, height="1000px", width="1500px")
    st.subheader("Selected item")
    st.write(timeline)


if __name__ == "__main__":
    vis_timeline()
