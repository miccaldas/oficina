"""Module Docstring"""
import snoop
from ranger import PY3
from ranger.api.commands import Command
from snoop import pp
import os

def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


class archivist(Command):
    """"""

    def execute(self):
        """"""



