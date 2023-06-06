"""
Module Docstring
"""
import numpy as np

# import matplotlib.pyplot as plt
import pandas as pd
import snoop
import streamlit as st
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


# MATPLOTLIB
# x = tagpython["time"]
# y = tagpython["ntid"]
# x1 = tagpandas["time"]
# y1 = tagpandas["ntid"]

# mt = plt.scatter(x, y)
# mt = plt.figure()
# fig, ax = plt.subplots()
# ax.plot(x, y, "o")
# ax.plot(x1, y1, "o")
# ax.scatter(x, y)
# ax.scatter(x1, y1)

# st.pyplot(fig)


@snoop
def pandas_tests():
    """"""
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

    # chart_data = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])
    # print(chart_data.dtypes)

    # timedf = timedf.set_index("tags")
    timedf["year"] = timedf["time"].dt.year
    timedf["month"] = timedf["time"].dt.month
    timedf["day"] = timedf["time"].dt.day
    timedf["hour"] = timedf["time"].dt.hour

    pd.set_option("display.max_rows", None)

    tt = timedf[["title", "tags", "time"]].copy()
    colvir = tt[tt["tags"].isin(["virtual", "columns"])]

    # tagpython = timedf.loc["python"]
    # yd = tagpython[(tagpython["year"] == 2021) & (tagpython["day"] == 19)]

    # tagpandas = timedf.loc[["pandas", "columns"]]
    # filterinDataframe = tagpandas[
    #     (tagpandas["year"] == 2021) & (tagpandas["month"] == 6)
    # ]
    # st.vega_lite_chart(
    #     tagpandas,
    #     {
    #         "mark": {"type": "circle"},
    #         "encoding": {
    #             "x": {"field": "time", "type": "temporal"},
    #             "y": {"field": "title", "type": "nominal"},
    #             "color": {"field": "tags", "type": "nominal"},
    #         },
    #     },
    #     use_container_width=True,
    # )

    st.vega_lite_chart(
        colvir,
        {
            "mark": {"type": "point"},
            "encoding": {
                "x": {"field": "time", "type": "temporal"},
                "y": {"field": "title", "type": "nominal"},
                "color": {"field": "tags", "type": "nominal"},
                "shape": {"field": "tags", "type": "nominal"},
            },
        },
        use_container_width=True,
    )


if __name__ == "__main__":
    pandas_tests()
