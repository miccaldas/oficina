"""
Some early tests that have some info worth keeping around.
"""
import pickle
import subprocess

import numpy as np
import pandas as pd
import snoop
import streamlit as st
from mysql.connector import Error, connect
from PIL import Image
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
        query = (
            "SELECT tag, COUNT(*) Total FROM(SELECT k1 as tag FROM notes UNION ALL SELECT k2 FROM notes UNION ALL SELECT k3 FROM notes) d GROUP BY tag ORDER BY TOTAL DESC LIMIT 10"
        )
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
def tag_lst():
    """
    Union allows to combine two or more sets of results into one, but,
    the number and order of columns that appear in the SELECT statement
    must be the same, and the data types must be equal or compatible.
    Union removes duplicates.
    """
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
        cur.execute(query)
        records = cur.fetchall()
        # Results come as one-element tuples. It's needed to turn it to list.
        records = [i for t in records for i in t]
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    with open("/home/mic/python/oficina/oficina/streamlit/taglst.bin", "wb") as f:
        pickle.dump(records, f)


@snoop
def selecttags():
    """
    We produce a list of tags. list of all post titles with
    the tag in k1 ,k2, or k3.
    """

    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes",
            # 'use_pure' denotes that we're using a Python implementation.
            use_pure=True,
        )
        cur = conn.cursor()
        # This query gets all the posts marked with a list of tags, in the k1, k2 and k3 column.
        query1 = "SELECT ntid, title, k1, k2, k3 FROM notes WHERE "
        query2 = "k1 = 'python' OR k1 = 'mysql' OR k1 = 'vim' OR k1 = 'sed' OR k1 = 'files' OR k1 = 'delete' "
        query3 = "OR k2 = 'python' OR k2 = 'mysql' OR k2 = 'vim' OR k2 = 'sed' OR k2 = 'files' OR k2 = 'delete' "
        query4 = "OR k3 = 'python' OR k3 = 'mysql' OR k3 = 'vim' OR k3 = 'sed' OR k3 = 'files' OR k3 = 'delete'"
        query = f"{query1}{query2}{query3}{query4}"
        # This formaulation gets the db data and turns it to a Panda's dataframe.
        posts_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    # So as to guarantee that the info collected in a widget can be used in another, we collect 'session_state' keys,
    # which are dictionary entries that keep the results of the widget. It'll be available for the duration of the
    # computer session. To instantiate them, it's needed to create these callback functions.
    def tag_option_callback():
        st.write(st.session_state.tag_choice)

    # This callback gathers the information of what tag the user wants to see the corresponding posts. The 'key' option
    # is needed to access session state.
    tag_option = st.selectbox(
        "Choose a keyword and see what posts are tagged with it.",
        ("python", "mysql", "vim", "sed", "files", "delete"),
        key="tag_choice",
    )

    # Now that we know what tag was chosen, we'll look into the dataframe built from the db's information, for posts with
    # this particaluar tag in the k1, k2, or k3 columns. The structure of this code is the following: The 'loc' option
    # after the dataframe's name defines that'll be searching by 'labels' or booleans. In this case, we'll look through the
    # columns labels, k1, k2, k3, for entries with the chosen tag. The '|' symbol in this context means 'OR'. A given tag
    # in k1, or k2, or k3.
    result = posts_dataframe.loc[(posts_dataframe["k1"] == tag_option) | (posts_dataframe["k2"] == tag_option) | (posts_dataframe["k3"] == tag_option)]

    # The checkox editable column widget from Streamlit, only accepts as values, False or True, without aspas. What this
    # means is that it's cumbersome to create a MySQL column just for this. The line below creates the editable checkbox
    # column, populated only of False values; so the user can choose a note by checking it, thus turning it into True.
    result["chkbx"] = False

    # We streamline the dataframe, so as to contain only the title, for the user to choose what note he wants to read, the
    # ntid, to search for the note file, and 'streamlit_checkbox', which is a new, purposefully built for Streamlit, column
    # in the notes db, in boolean format with a default value of False. The user chooses a note by turning the checkbox value
    # from False to True.
    res_title = result[["ntid", "title", "chkbx"]]

    # The session variable that'll house the ntid that the user will choose to see the note.
    def choice_id_callback():
        st.write(st.session_state.choiceid)

    # So as to have an editable column that the user could interact with, it was needed the 'data_editor' widget, that houses
    # a lot of editable content, specifically, an editable checkbox column. We populate the fields with our more current
    # dataframe, assure that the table has the same width as the tag dropdown, instantiate the state session key, and define
    # the checkbox column's title, help suggestions and set the default value as False.
    choice_id = st.data_editor(
        res_title,
        use_container_width=True,
        hide_index=True,
        key="choiceid",
        column_config={
            "shownote": st.column_config.CheckboxColumn(
                "Choose",
                help="Check a note you would like to see.",
                default=False,
            )
        },
    )

    # The note that the user chose, by clicking the checkbox column, is found by looking for the last checked value in the
    # 'chkbx' column. This defines not a value, but a Panda's artefact called 'Series', that is a one dimensional array,
    # with a series of values. The one we're interested in is the first one, the 'ntid' value. As Pandas doesn't accept the
    # 'if' clause that is used to compare booleans to the True value, (if a is True ...), there was no direct way to define
    # the choice made by the user. But it just so happens that 1 is another representation of True, and this is accepted by
    # Pandas. So, the 'chosen_note' definition was changed, and a long, complicated problem is no more.
    chosen_note = choice_id.loc[(choice_id["chkbx"] == 1)]["ntid"]
    chosen_ntid = chosen_note.values[0]

    # As there's no way to upload documents to Streamlit, but it's possible to send images, we convert the notes' text files to GIF
    # format images, as is one of the must supported image formats for 'pango-view'.
    cmd = f'pango-view --dpi=120 --font="mono" -qo {chosen_ntid}.gif {chosen_ntid}.txt'
    subprocess.run(cmd, cwd="/home/mic/python/notes/notes/notes/", shell=True)

    # Insert a divider, for pretiness sake.
    st.divider()

    # Finally we open the note image in the Streamlit site.
    img = Image.open(f"/home/mic/python/notes/notes/notes/{chosen_ntid}.gif")
    st.image(img)


if __name__ == "__main__":
    selecttags()
