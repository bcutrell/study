from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, DataTable

ROWS = [
    ("task", "time", "status"),
    ("Write code", "3h", "done"),
    ("Test code", "1h", "done"),
    ("Fix bugs", "2h", "in progress"),
]

class MyApp(App):
    """ A Textual App to monitor files. """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

if __name__ == "__main__":
    app = MyApp()
    app.run()