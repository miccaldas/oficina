"""
Create a Streamlit app with data from the note's database.
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
def tag_lst():
    """
    Union allows to combine two or more sets of results into one, but,
    the number and order of columns that appear in the SELECT statement
    must be the same, and the data types must be equal or compatible.
    Union removes duplicates.
    """
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes",
            use_pure=True,
        )
        # As were using the Pandas version of MySQL connection, there were problems wiuth this query, as it
        # is, probably lazy loaded, and the selection/union operations in different columns, was making it
        # that it was loosing results. The solution is to add 'buffered=true' to the 'cur' line.
        cur = conn.cursor(buffered=True)
        query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
        cur.execute(query)
        tags_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return tags_dataframe


@snoop
def selecttags():
    """
    We produce a list of tags. User chooses one, we'll search the db
    for posts that contain it. Present the results and if the user so
    wishes, he can select one the ntid's and we'll show him the note.
    """

    tags_dataframe = tag_lst()

    # So as to guarantee that the info collected in a widget can be used in another, we collect 'session_state' keys,
    # which are dictionary entries that keep the results of the widget. It'll be available for the duration of the
    # computer session. To instantiate them, it's needed to create these callback functions.
    def tag_option_callback():
        st.write(st.session_state.tag_choice)

    # This callback gathers the information about what tag the user selects. The 'key' option is needed to access
    # the session state. 'Index' is Pandas' id for the tag entry, that's preselected,  and visible on the selectbox.
    tag_option = st.selectbox(
        "Choose a keyword and see what posts are tagged with it.",
        tags_dataframe,
        key="tag_choice",
        index=1,
    )

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
        # The '||' symbol in SQL stands for 'OR'.
        query = f"SELECT ntid, title FROM notes WHERE k1 = '{tag_option}' || k2 = '{tag_option}' || k3 = '{tag_option}'"
        # This formaulation gets the db data and turns it to a Panda's dataframe.
        result = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    # The checkox editable column widget from Streamlit, only accepts as values False or True, without aspas. It's cumbersome
    # to create a MySQL column just for this. The line below creates the editable checkbox column, populated only by False
    # values. This way, when the user chooses a note, it evaluates to 'true', which is the trigger to show the note's text.
    result["chkbx"] = False

    # We streamline the dataframe, so as to contain only the title, for the user to choose, the ntid, to search for the file,
    # and 'streamlit_checkbox', which is a new, purposefully built for Streamlit, column in the notes db, in boolean format
    # with a default value of False. The user chooses a note by turning the checkbox value from False to True.
    res_title = result[["ntid", "title", "chkbx"]]

    # Just so people don't see an error message when entering the app, because there's no entry selected, I changed the boolean
    # value of one of the ever visible options on the selectbox, to "true". That way it already shows note content. The 'at'
    # option denotes location, as 'loc', and is composed of its Pandas index and column name.
    res_title.at[0, "chkbx"] = True

    # The session variable that'll house the ntid's note chosen by the user.
    def choice_id_callback():
        st.write(st.session_state.choiceid)

    # The 'date_widget' was chosen so as to have an editable column that the user could interact with. It houses
    # a lot of editable content, specifically, an editable checkbox column. We populate the fields, assure that
    # the table has the same width as the tag Dropdown, instantiate the state session key, define the checkbox
    # column's title, help suggestions, and set the default value as False.
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

    # The user's note choice, is found by looking for the last checked value in the 'chkbx' column. This defines not a value,
    # but a Panda's artefact called 'Series', that is a one dimensional array, with a series of values. The one we're
    # interested in is the first one, the 'ntid' value. Here 1 is another representation of 'true' accepted by Pandas.
    chosen_note = choice_id.loc[(choice_id["chkbx"] == 1)]["ntid"]
    chosen_ntid = chosen_note.values[0]

    # As there's no way to upload documents to Streamlit, we'll convert the note's text files to GIF's, as is one of the
    # must supported image formats for 'pango-view', that we're using to make the conversion.
    cmd = f'pango-view --dpi=120 --font="mono" -qo {chosen_ntid}.gif {chosen_ntid}.txt'
    subprocess.run(cmd, cwd="/home/mic/python/notes/notes/notes/", shell=True)

    # Insert a divider, for pretiness sake.
    st.divider()

    # Finally we open the note image in the Streamlit site.
    img = Image.open(f"/home/mic/python/notes/notes/notes/{chosen_ntid}.gif")
    st.image(img)


if __name__ == "__main__":
    selecttags()
