"""
Module that collects, treats and publishes, the information
that'll be used in Streamlit's timeline widget. It's called
by 'notes_by_tag.py'.
"""
import json

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
def db_items(tag_option):
    """
    Collects data from the db. Uses column aliases
    to match Streamlit-timeline's column's names.
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
        query = f"SELECT idx AS id, title, tags AS content, time AS start FROM tags_streamlit WHERE tags = '{tag_option}'"
        td = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    dataframe_to_dict(td)


# @snoop
def dataframe_to_dict(td):
    """
    Converts dataframe to dictionary. Because the
    'start' column has a 'datetime' format, which
    is not accepted by the widget, we need to turn
    its values into strings.
    """
    td["start"] = td["start"].astype("str")
    tdict = td.to_dict("records")

    vis_timeline(tdict)


@snoop
def vis_timeline(tdict):
    """
    Publishes the timeline.
    """
    timeline = st_timeline(tdict, groups=[], options={}, height="400px", width="700px")
    st.subheader("Selected item")
    st.write(timeline)
