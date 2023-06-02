"""
Create a Streamlit app with data from the note's database.
"""
import pickle

import pandas as pd
import snoop
import streamlit as st
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def notes_test1():
    """
    We'll use Panda and Streamlit to create a web app
    that shows the db's tags, click one and you'll
    see the titles of the tagged posts, click one and
    it'll open the note.
    """

    notedf = pd.read_pickle("notesdf.bin")

    st.dataframe(notedf.style.highlight_max(axis=0))


# if __name__ == "__main__":
#     notes_test1()


@snoop
def notes_test2():
    """
    Counts the number of tag results in the
    k1, k2, k3 columns. Keeps only the first
    10 results.
    Sends it to a Panda's dataframe.
    """

    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes",
            use_pure=True,
        )
        cur = conn.cursor()
        query = "SELECT tag, COUNT(*) Total FROM(SELECT k1 as tag FROM notes UNION ALL SELECT k2 FROM notes UNION ALL SELECT k3 FROM notes) d GROUP BY tag ORDER BY TOTAL DESC LIMIT 10"
        tags_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    st.line_chart(tags_dataframe, x="Total", y="tag")


# if __name__ == "__main__":
#     notes_test2()


@snoop
def selecttags():
    """
    User chooses from a list of tags, one.
    Returns list of all post titles with
    the tag in k1 ,k2, or k3.
    """

    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes",
            use_pure=True,
        )
        cur = conn.cursor()
        query1 = "SELECT ntid, title, k1, k2, k3 FROM notes WHERE "
        query2 = "k1 = 'python' OR k1 = 'mysql' OR k1 = 'vim' OR k1 = 'sed' OR k1 = 'files' OR k1 = 'delete' "
        query3 = "OR k2 = 'python' OR k2 = 'mysql' OR k2 = 'vim' OR k2 = 'sed' OR k2 = 'files' OR k2 = 'delete' "
        query4 = "OR k3 = 'python' OR k3 = 'mysql' OR k3 = 'vim' OR k3 = 'sed' OR k3 = 'files' OR k3 = 'delete'"
        query = f"{query1}{query2}{query3}{query4}"
        posts_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    def tag_option_callback():
        st.write(st.session_state.tag_choice)

    tag_option = st.selectbox(
        "Choose a keyword and see what posts are tagged with it.",
        ("python", "mysql", "vim", "sed", "files", "delete"),
        key="tag_choice",
    )

    result = posts_dataframe.loc[
        (posts_dataframe["k1"] == tag_option)
        | (posts_dataframe["k2"] == tag_option)
        | (posts_dataframe["k3"] == tag_option)
    ]

    res_title = result[["ntid", "title"]]

    st.dataframe(res_title, use_container_width=True)


if __name__ == "__main__":
    selecttags()
