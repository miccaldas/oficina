"""
Module Docstring
"""
import snoop
from dotenv import load_dotenv
from snoop import pp
from textual.app import App, ComposeResult
from textual.events import Key

# import os
from textual.widgets import Button, Header, Label, Welcome


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


class QuestionApp(App[str]):
    CSS_PATH = "question2.css"
    TITLE = "A Question App"
    SUB_TITLE = "Most Import Question"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Do you love Textual?", id="question")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

    def on_key(self, event: Key):
        self.title = event.key
        self.sub_title = f"You just pressed {event.key}"


if __name__ == "__main__":
    app = QuestionApp()
    reply = app.run()
    print(reply)
