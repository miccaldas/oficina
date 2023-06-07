"""
Just a home for some Pandas experiments, that turned out to be Vega-lite experiments.
"""
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import snoop
import streamlit as st
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def db_data():
    """
    Collects db data.
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
def time_df():
    """
    Base dataframe for the experiments. Added time intervals
    columns so would be easier to manipulate.
    """
    timedf = db_data()

    # This extracts time intervals from the 'time' column. Pandas' datetime format has
    # other intervals like 'Quarter', etc.
    timedf["year"] = timedf["time"].dt.year
    timedf["month"] = timedf["time"].dt.month
    timedf["day"] = timedf["time"].dt.day
    timedf["hour"] = timedf["time"].dt.hour

    # This, when printing, makes it that it prints all of the dataframe.
    pd.set_option("display.max_rows", None)

    return timedf


@snoop
def see_tag_selection():
    """
    Creates dataframe from 'timedf'. Presents data of two tags only.
    """
    timedf = time_df()

    # Create a new dataframe from the columns, 'title', 'tags' and 'time'.
    tt = timedf[["title", "tags", "time"]].copy()

    # From the former selection, I drilled even further, so as to have only rows
    # that have the 'virtual' and 'columns' tags.
    colvir = tt[tt["tags"].isin(["virtual", "columns"])]

    # This is the widget of 'Vega-lite', an interactive graphics library, for Streamlit
    # 'mark' is the type of point you'll use to mark the entries, and 'encoding', defines:
    # Axes - (x, y), where 'fields' is the dataframe column you want to use and type is
    #        refers if the value is:
    #            temporal(datetime),
    #            nominal(many things, but mainly string),
    #            quantitative(integers), and others.
    # Color - If you want to have different colors for different data points, as the
    #         'virtual' and 'columns' tags, you just tell it what column you want and it'll
    #         color it automatically.
    # Shape - If you want different shapes for different data points. As for 'color', you
    #         just tell it the column and it does the rest.
    # 'use_container_width', is comon in Streamlit widgets, and serves to align widget width.
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


@snoop
def dataframe_per_tag():
    """
    Experiments in creating dataframes from tag data.
    """
    timedf = time_df()

    # Tried to set 'tags' as index, but that meant that I couldn't use them as value.
    # Anyway, this is what I've done with it.
    timedf = timedf.set_index("tags")

    # Creates a dataframe using the index/tag 'python'. Only 'python' values are returned.
    tagpython = timedf.loc["python"]
    # Creates dataframe that only has data on posts with the tag 'python', from the day 19,
    # any month, in 2021.
    yd = tagpython[(tagpython["year"] == 2021) & (tagpython["day"] == 19)]

    # Creates dataframe from the indexes/tags 'pandas' and 'columns'.
    tagpandas = timedf.loc[["pandas", "columns"]]
    # Filters 'tagpandas' data, to present only info from the month 6 of 2021.
    filterinDataframe = tagpandas[(tagpandas["year"] == 2021) & (tagpandas["month"] == 6)]
    # Uses Streamlit's 'Vega-lite' widget to create a scatter graphic of note's titles in a
    # time axis.
    st.vega_lite_chart(
        tagpandas,
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {"field": "time", "type": "temporal"},
                "y": {"field": "title", "type": "nominal"},
                "color": {"field": "tags", "type": "nominal"},
            },
        },
        use_container_width=True,
    )


@snoop
def matplotlib_experiments():
    """
    At first I wasn't able to make the 'Vega-lite' widget work,
    so I tried other things. One thing I tried is 'Matplotlib'.
    Vega-lite is better, but Matplotlib is ubiquitous and won't
    hurt knowing a little more about it.
    """
    timedf = time_df()

    # Creates a dataframe using the index/tag 'python'. Only 'python' values are returned.
    tagpython = timedf.loc["python"]
    # Creates dataframe from the indexes/tags 'pandas' and 'columns'.
    tagpandas = timedf.loc[["pandas", "columns"]]

    # To show more than one data series on Matplotlib, in a scatter graphic, you have to define
    # (x, y) axis for each one. For 'tagpython' and 'tagpandas', in this case.
    x = tagpython["time"]
    y = tagpython["ntid"]
    x1 = tagpandas["time"]
    y1 = tagpandas["ntid"]
    # This defines the graphic type.
    mt = plt.scatter(x, y)
    # This defines the result as a 'Figure', which I didn't really get what it is, but you really need
    # it if you're going to use the Streamlit widget.
    mt = plt.figure()
    # This, again, is necessary for Streamlit, and it theoretically is used to present several graphics
    # even if t's not the cae here. I repeat, it won't work any other way.
    fig, ax = plt.subplots()
    # This 'draws' the data on the plot. The lone 'o' indicates the format of you mark.
    ax.plot(x, y, "o")
    ax.plot(x1, y1, "o")
    # Draws data in a scatter plot.
    ax.scatter(x, y)
    ax.scatter(x1, y1)
    # Sends result to Streamlit.
    st.pyplot(fig)


@snoop
def vegacount():
    """
    Trying's Vega's 'count' data tranformations.
    """
    timedf = time_df()

    # From 'timedf' it takes only entries with these tags.
    tagpython = timedf[timedf["tags"].isin(["python", "mysql", "lists", "sed", "sqlite"])]

    # Creates new dataframe that bins (by counting number of rows in group),'tags'
    # values in a 'string_date' timeframe. It displays them by creating a 'count'
    # column and making it the index.
    # I first thought of this to be used
    # with a 'year-month' date type, which would be created by this code:
    # "tagpython["ymonth"] = tagpython["time"].dt.to_period("M")".
    # But the 'ymonth' column that it originated has a 'period' type, not 'datetime';
    # and Vega-lite didn't understood it. Regardless, the new 'count' column, allowed us
    # the use of the 'aggreagate' function. This summed the tags posted in the time
    # period, as defined by 'yearmonth': another Vega function, that 'bins' datetime
    # data in months on a year.
    tm = tagpython.groupby(["tags", "time"]).size().reset_index(name="count")

    # Creates new dataframe selected by this list of tags. isin() is useful to select
    # several values from the same column.
    tgcnt = tm[tm["tags"].isin(["python", "mysql", "lists", "sed", "sqlite"])]

    # Here Vega-lite does much of the heavy lifting. The 'x' axis will be defined by
    # Vega using its 'yearmonth' construct, that creates a date defined to the month,
    # from data on the 'time' column. With it we can sum the 'count' results per month,
    # using Vega-lite's 'aggregate' function.
    st.vega_lite_chart(
        tgcnt,
        {
            "mark": {"type": "line", "point": True},
            "encoding": {
                "x": {"timeUnit": "yearmonth", "field": "time"},
                "y": {"aggregate": "count"},
                "color": {"field": "tags", "type": "nominal"},
            },
        },
        use_container_width=True,
    )


@snoop
def string_dates():
    """
    Tags in a time axis, without using Vega-lite date awareness,
    or Pandas' datetime columns.
    """
    timedf = time_df()

    # From 'timedf' it takes only entries with these tags.
    tagpython = timedf[timedf["tags"].isin(["python", "mysql", "lists", "sed", "sqlite"])]

    # We create variables with the month and year values used to filter the data,
    # so we can easily insert them in the title.
    yr = 2022
    mnth = 2

    # This creates a dataframe with data from the chosen year and month.
    choice = tagpython.query(f"year == {yr} & month == {mnth}")

    # Don't use Vega-lite 'title' option when using Streamlit. It'll behave in
    # strange ways, as moving the gra+hic to the right and, when trying to position
    # the title, move the graphic instead.
    st.header(f"Notes Created on {mnth}-{yr}")

    # Note the use of the 'day' column as 'x', since we already selected by year and month.
    st.vega_lite_chart(
        choice,
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {"field": "day", "type": "nominal"},
                "y": {"field": "title", "type": "nominal"},
                "color": {"field": "tags", "type": "nominal"},
            },
        },
        use_container_width=True,
    )


@snoop
def pandascount():
    """
    Similar to 'vegacount' but only using Pandas
    to manipulate data. Here Vega-lite only shows
    the data.
    """
    timedf = time_df()

    # From 'timedf' it takes only entries with these tags.
    tagpython = timedf[
        timedf["tags"].isin(
            [
                "python",
                "mysql",
                "lists",
                "sed",
                "sqlite",
                "dataframes",
                "dictionary",
                "files",
            ]
        )
    ]

    # This, when printing, makes it that it prints all of the dataframe.
    pd.set_option("display.max_rows", None)

    # Creates new dataframe that bins (by counting number of rows in group),'tags'
    # values in a 'string_date' timeframe. It displays them by creating a 'count'
    # column and making it the index.
    tm = tagpython.groupby(["tags", "string_date"]).size().reset_index(name="count")

    # Presents dataframe data by the 'count' column, in ascending order.
    tm = tm.sort_values(by=["count"])

    st.vega_lite_chart(
        tm,
        {
            "mark": {"type": "bar"},
            "encoding": {
                "x": {"field": "count", "type": "quantitative"},
                "y": {"field": "string_date", "type": "nominal"},
                "color": {"field": "tags", "type": "nominal"},
            },
        },
        use_container_width=True,
    )


@snoop
def notesdb():
    """
    Downloads and treats data from the 'notes' table,
    to make some experiments with Pandas correlation
    functions. I need a column with the three note
    tags in a tuple, and couldn't figure out how to do
    it. So I downloaded the data the old fashioned way,
    created the column and oly then created the dataframe.
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
        query = "SELECT * FROM notes"
        cur.execute(query)
        notedata = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    # List to house the results.
    newdata = []
    # If you try to change the 'ntid' value to string, as you must for the comprehension,
    # it wont let you because each row is a tuple and this only works for lists. So first
    # we turn each row into a list.
    rowlst = [[i] for i in notedata]
    # Then we iterate through them:
    for i in rowlst:
        # We turn 'ntid' into a string and create a new tuple with the values of 'k1/2/3'.
        tagtuple = [(str(a), b, c, d, e, (c, d, e), f) for a, b, c, d, e, f in i]
        # We then put it in final list, making sure that we remove it from the list created
        # in 'rowlst'. It served its purpose, whch was to allow us to change 'ntid's type.
        newdata.append(tagtuple[0])

    # Create the dataframe.
    ndf = pd.DataFrame(newdata, columns=["ntid", "title", "k1", "k2", "k3", "tags", "time"])

    # Finally we pickle the dataframe, as these operations are slow and I son't want to run
    # this everytime I'm trying something.
    ndf.to_pickle("ndf.bin")


# if __name__ == "__main__":
#     notesdb()


@snoop
def correlation():
    """
    This was supposed to be experiments with Pandas correlation
    functions. But all its methods are quantitative, and since
    all my data is qualitative, I went to rabbit hole to see what
    I could use. I found this, although not completely sure what
    'this' is.
    """
    ndf = pd.read_pickle("ndf.bin")

    # From here on out, most code was taken from here: https://tinyurl.com/2qgekhdx
    confusion_matrix = pd.crosstab(ndf["title"], ndf["k3"])

    # This, when printing, makes it that it prints all of the dataframe.
    pd.set_option("display.max_rows", None)

    print(confusion_matrix)

    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.to_numpy().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    print(np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1))))


@snoop
def pandascount_heatmap():
    """
    Starting from 'pandascount', create a heatmap.
    """
    timedf = time_df()

    # From 'timedf' it takes only entries with these tags.
    tagpython = timedf[
        timedf["tags"].isin(
            [
                "python",
                "mysql",
                "lists",
                "sed",
                "sqlite",
                "dataframes",
                "dictionary",
                "files",
            ]
        )
    ]

    # This, when printing, makes it that it prints all of the dataframe.
    pd.set_option("display.max_rows", None)

    # Creates new dataframe that bins (by counting number of rows in group),'tags'
    # values in a 'string_date' timeframe. It displays them by creating a 'count'
    # column and making it the index.
    tm = tagpython.groupby(["tags", "string_date"]).size().reset_index(name="count")

    st.vega_lite_chart(
        tm,
        {
            "mark": {"type": "rect"},
            "encoding": {
                "x": {"field": "string_date", "type": "nominal"},
                "y": {"field": "tags", "type": "nominal"},
                "color": {"field": "count", "type": "quantitative"},
            },
        },
        use_container_width=True,
    )


@snoop
def posts_per_hour():
    """
    What hours are historicallly better for posting?
    """
    timedf = time_df()

    # Creates new dataframe that bins (by counting number of rows in group),'tags'
    # values in a 'hour' timeframe. It displays them by creating a 'count'
    # column and making it the index.
    tm = timedf.groupby(["hour", "tags"]).size().reset_index(name="count")
    # Counts how many times a specific hour is repeated. Creates a Series.
    hours = tm["hour"].value_counts()
    # Turns the Series to a Dataframe.
    hours = hours.to_frame()
    # Renames the 'hour' column to count, 'axis=1' says that this value is in the 'x'
    # axis and 'inplace', being True, tells it to not create new dataframe but change
    # this one.
    hours.rename({"hour": "count"}, axis=1, inplace=True)
    # Creates a new column 'hr' from the index. This is necessary because when we used
    # value_counts() to get the count of the hours, it used the 'hour' values column as
    # as index. Which means we can not access them, unless, as we do here, we copy them
    # to a new column.
    hours["hr"] = hours.index

    # This, when printing, makes it that it prints all of the dataframe.
    pd.set_option("display.max_rows", None)
    print(hours.info(verbose=True))

    st.vega_lite_chart(
        hours,
        {
            "mark": {"type": "bar"},
            "encoding": {
                "x": {"field": "hr", "type": "quantitative"},
                "y": {"field": "count", "type": "quantitative"},
            },
        },
        use_container_width=True,
    )


@snoop
def tags_per_hour():
    """
    Thr hours of the day that tags are published.
    """
    timedf = time_df()

    # Creates new dataframe that bins (by counting number of rows in group),'tags'
    # values in a 'hour' timeframe. It displays them by creating a 'count'
    # column and making it the index.
    tm = timedf.groupby(["hour", "tags"]).size().reset_index(name="count")
    # We set the 'tags' column as index, so we can easily select with its values;
    # making sure that we keep them as a column, through the 'drop=False' argument.
    sedf = tm.set_index(keys="tags", drop=False)
    # We define a new dataframe with all the rows that contain any of the tags in this list.
    sample = sedf[
        sedf["tags"].isin(
            [
                "sed",
                "python",
                "mysql",
                "lists",
                "sqlite",
                "dataframes",
                "dictionary",
                "files",
            ]
        )
    ]

    # st.vega_lite_chart(
    #     sample,
    #     {
    #         "mark": {"type": "bar"},
    #         "point": True,
    #         "encoding": {
    #             "x": {"field": "hour", "type": "quantitative"},
    #             "y": {
    #                 "aggregate": "sum",
    #                 "field": "count",
    #                 "type": "quantitative",
    #                 "stack": "normalize",
    #             },
    #             "color": {
    #                 "field": "tags",
    #                 "type": "nominal",
    #                 "scale": {
    #                     "range": [
    #                         "#675193",
    #                         "#ca8861",
    #                         "#F99B7D",
    #                         "#E76161",
    #                         "#B04759",
    #                         "#8BACAA",
    #                         "#080202",
    #                         "#9E6F21",
    #                     ]
    #                 },
    #             },
    #         },
    #     },
    #     use_container_width=True,
    # )

    """
    The reason the Streamlit code is commented is because, after trying it out, it became increasingly obvious that it has serious
    limitations, specifically in what pertains to width. Everything is bunched up and, unless you're using a very small number of
    rows, it's very visually unappealing. I'm going to try to use Vega-lite directly to a 'localhost' page, to see if it looks better.
    Anyway, I'm just going to convert the dataframe to a dictionary, which is what Vega-lite really uses, and try this another way.
    """

    sampledict = sample.to_dict("records")
    with open("sampledict.bin", "wb") as f:
        pickle.dump(sampledict, f)
