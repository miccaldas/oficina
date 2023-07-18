"""
Module Docstring
"""
import snoop

# import os
# import subprocess
from dotenv import load_dotenv
from snoop import pp
from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Static


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


class ColorApp(App):
    def compose(self) -> ComposeResult:
        self.widget1 = Static("Textual One")
        yield self.widget1
        self.widget2 = Static("Textual Two")
        yield self.widget2
        self.widget3 = Static("Textual Three")
        yield self.widget3

    def on_mount(self) -> None:
        self.widget1.styles.background = "#A1CCD1"
        self.widget2.styles.background = "#E9B384"
        self.widget2.styles.color = "#7C9D96"
        self.widget3.styles.background = "#F4F2DE"


if __name__ == "__main__":
    app = ColorApp()
    app.run()
