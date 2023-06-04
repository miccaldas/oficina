"""
Exploring timelines, notes' data and Streamlint.
"""
import datetime
import pickle

import numpy as np
import pandas as pd
import snoop
import streamlit as st
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def notes_by_date():
    """
    Collects and pickles notes' db content.
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
        query = "SELECT * FROM tags_streamlit"
        cur.execute(query)
        timedf = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return timedf


@snoop
def set_date():
    """
    Creates a datetime column, divided by year-month, from the
    earliest post entry to the last.
    """
    time_dataframe = notes_by_date()
    td = time_dataframe

    # Creation of the 'start_date' column. It'll show month and year.
    # It tells to consider the value in the column 'time' and
    # create a 'start_date' column, taking the value of 'time', but
    # just to the month level. 'dt' is short for 'dataframe' and is
    # an official designation.
    td["start_date"] = pd.to_datetime(td["time"]).dt.to_period("M")

    return td


@snoop
def upload_changes_to_db():
    """
    Uploads the dataframe with the new
    data to the db.
    """
    td = set_date()

    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes",
            use_pure=True,
        )
        cur = conn.cursor(buffered=True)
        # This generates a list of all index values in the dataframe
        index_values = list(td.index.values)
        for id in index_values:
            value = td.loc[id, "start_date"]
            query = f"UPDATE tags_streamlit SET datetime_date = '{value}' WHERE id_comp = {id}"
            cur.execute(query)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    upload_changes_to_db()
