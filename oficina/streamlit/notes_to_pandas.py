"""
Downloads notes' data directly to a Panda's dataframe
"""
import pandas as pd
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def notes_to_pandas():
    """
    This code downloads db's information into a panda's dataframe
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
        query = "SELECT ntid, title, k1, k2, k3 FROM notes"
        result_dataframe = pd.read_sql(query, conn)
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    # Pickles the dataframe
    result_dataframe.to_pickle("notesdf.bin")


if __name__ == "__main__":
    notes_to_pandas()
