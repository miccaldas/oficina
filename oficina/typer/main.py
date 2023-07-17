"""
Module Docstring
"""
import snoop

# import os
# import subprocess
import typer
from rich import print
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


data = {
    "name": "Rick",
    "age": 42,
    "items": [{"name": "Portal Gun"}, {"name": "Plumbus"}],
    "active": True,
    "affiliation": None,
}


# @snoop
def main():
    """"""
    print(data)


if __name__ == "__main__":
    typer.run(main)
