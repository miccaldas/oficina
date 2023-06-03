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
        query = "SELECT ntid, title, k1, k2, k3, time FROM notes"
        cur.execute(query)
        time_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    time_dataframe.to_pickle("time.bin")
    return time_dataframe


@snoop
def set_month():
    """
    Creates a datetime column, divided by year-month, from the
    earliest post entry to the last.
    Sets new column as index.
    """
    time_dataframe = notes_by_date()
    td = time_dataframe

    # Creation of the 'month' column. It'll show month and year.
    td["month"] = pd.to_datetime(td["time"]).dt.to_period("M")

    # We'll pickle it, just so it's easier to access it.
    td["month"].to_pickle("month.bin")

    # Sets 'month' as index.
    td = td.set_index(["month"])

    return td


@snoop
def divide_by_month():
    """
    Divide data by month.
    """
    td = set_month()

    mthlst = [
        "2023-03",
        "2020-12",
        "2021-01",
        "2021-02",
        "2021-03",
        "2021-04",
        "2021-05",
        "2021-06",
        "2021-07",
        "2021-08",
        "2021-09",
        "2021-10",
        "2021-11",
        "2021-12",
        "2022-01",
        "2022-02",
        "2022-04",
        "2022-05",
        "2022-08",
        "2023-01",
        "2023-02",
        "2023-04",
        "2023-05",
        "2023-06",
    ]

    series = []
    for i in mthlst:
        data = td.loc[i]
        # Aggregate tags in the 3 tags columns to one column.
        # In the months were there was just one post, the command to
        # concatenate would fail, as there was nothing to concatenate
        # to. To remedy this we constructed a try/except block to
        # reconstruct a pandas series with just one entry.
        try:
            serie = pd.concat([data["k1"], data["k2"], data["k3"]])
            series.append(serie)
        except (KeyError, TypeError):
            # First we create a dictionary with the 'month' data and
            # the info from k1, k2 and k3. Our objective is to build
            # a dataframe to house this line of information, and its
            # easier done through a dictionary than through a string.
            uni = {"month": i, "tags": [data[2], data[3], data[4]]}
            # To turn it to a real dictionary, using 'eval', that
            # preffers strings as input, we convert it to one.
            unistr = str(uni)
            # Only now can we build it as a true dictionary, with eval.
            ndic = eval(unistr)
            # We turn to dict to a Dataframe.
            uni_dataframe = pd.DataFrame(ndic)
            # And so as to be equal with all the other data, we make of
            # 'month', the index.
            uni_dataframe = uni_dataframe.set_index(["month"])
            # Finally we add all the months data into one list.
            series.append(uni_dataframe)
    with open("series.bin", "wb") as d:
        pickle.dump(series, d)

    return series


@snoop
def add_tags():
    """
    Where we'll do what we wanted to do in the last module but couldn't.
    It was created a new Mysql table, 'tags_streamlit', that gathers all
    the tags in one column, accompanied by a 'time' column with their
    corresponding timestamps. We'll query the table for the tags, divided
    by month and year.
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
        query = "SELECT k1, title, YEAR(time) AS year, MONTH(time) AS month, COUNT(*) AS count FROM tags_streamlit GROUP BY k1, title, YEAR(time), MONTH(time)"
        cur.execute(query)
        tags_time_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    tags_time_dataframe.to_pickle("tags_streamlit.bin")


if __name__ == "__main__":
    add_tags()
