"""
Module Docstring
"""
import snoop

# import os
# import subprocess
from dotenv import load_dotenv
from snoop import pp
from textual.app import App, ComposeResult
from textual.widgets import Static


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

TEXT = """
I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain.
"""


class DimensionsApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Static(TEXT)
        yield self.widget

    def on_mount(self) -> None:
        self.widget.styles.background = "purple"
        self.widget.styles.width = "60vw"
        self.widget.styles.height = "60vh"


if __name__ == "__main__":
    app = DimensionsApp()
    app.run()
