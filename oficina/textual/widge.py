"""
Module Docstring
"""
import snoop
from dotenv import load_dotenv
from snoop import pp
from textual.app import App, ComposeResult

# import os
from textual.widgets import Button, Welcome


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


class WelcomeApp(App):
    def on_key(self) -> None:
        self.mount(Welcome())
        self.query_one(Button).label = "YES!"
        self.exit()


if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
