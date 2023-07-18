"""
Module Docstring
"""
import snoop

# import os
# import subprocess
from dotenv import load_dotenv
from snoop import pp
from textual import events
from textual.app import App


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


class EventApp(App):
    COLORS = [
        "white",
        "maroon",
        "red",
        "purple",
        "fuchsia",
        "olive",
        "yellow",
        "navy",
        "teal",
        "aqua",
    ]

    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"

    def on_key(self, event: events.Key) -> None:
        if event.key.isdecimal():
            self.screen.styles.background = self.COLORS[int(event.key)]


if __name__ == "__main__":
    app = EventApp()
    app.run()
