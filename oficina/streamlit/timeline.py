"""
Module Docstring
"""
from json import dumps, loads

import numpy as np
import pandas as pd
import snoop
import streamlit as st
from snoop import pp
from streamlit_timeline import timeline


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def json_file():
    """"""
    streamdata = pd.read_pickle("tags_streamlit.bin")
    print(streamdata)


if __name__ == "__main__":
    json_file()
