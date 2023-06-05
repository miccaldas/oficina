"""
Module Docstring
"""
import pandas as pd
import plotly.express as px
import snoop
from dash import Dash, Input, Output, callback, dcc, html
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1(children="A Very Nice Title", style={"textAlign": "center"}),
        dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
        dcc.Graph(id="graph-content"),
    ]
)


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


if __name__ == "__main__":
    app.run_server(debug=True)
