"""
Module Docstring
"""
import snoop
from dash import Dash, html

# from configs.config import Efs, tput_config
# import os
# import subprocess
from dotenv import load_dotenv
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


app = Dash(__name__)
app.layout = html.Div([html.Div(children="hello world")])


if __name__ == "__main__":
    app.run_server(debug=True)
