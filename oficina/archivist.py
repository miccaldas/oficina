"""Module Docstring"""
import os
import subprocess

import snoop
from ranger import PY3
from ranger.api.commands import Command
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


class archive(Command):
    @snoop
    def execute(self):
        """"""

        path = f"{self.fm.thisdir}/{self.fm.thisfile}"
        cmd = f"atool -x {path}"
        subprocess.run(cmd, shell=True)

    if __name__ == "__main__":
        execute()
