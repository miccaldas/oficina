"""
Module Docstring
"""
import pandas as pd
import plotly.express as px
import snoop
from dash import Dash, dash_table, dcc, html
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


app = Dash(__name__)
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)
# App layout
app.layout = html.Div(
    [
        html.Div(children="My First App with Data and a Graph"),
        dash_table.DataTable(data=df.to_dict("records"), page_size=10),
        dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
