"""
Trying to learn some Textual...

Awesome libraries
    mysql monitor -> https://github.com/charles-001/dolphie
    cooler $ top  -> https://github.com/nschloe/tiptop
    SQL ide       -> https://github.com/tconbeer/harlequin

Resources
https://dev.to/wiseai/textual-the-definitive-guide-part-3-2gl
https://textual.textualize.io/styles/grid/#__tabbed_1_1
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, DataTable, TabbedContent, Tab, Static, Tree
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

ROWS = [
    ("task", "time", "status"),
    ("Write code", "3h", "done"),
    ("Test code", "1h", "done"),
    ("Fix bugs", "2h", "in progress"),
]

class Menu(TabbedContent, can_focus=True):
    BORDER_TITLE = "Data Catalog"

    BINDINGS = [
        Binding("j", "switch_tab(-1)", "Previous Tab", show=False),
        Binding("k", "switch_tab(1)", "Next Tab", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Tab("Tables", id="tables")
        yield Tab("Views", id="views")
        yield Tab("Procedures", id="procedures")
        yield Tab("Functions", id="functions")

    def on_mount(self) -> None:
        self.border_title = "Data Catalog"

class MyApp(App):
    """ A Textual App to monitor files. """

    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        tree: Tree[dict] = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")

        vs = VerticalScroll(id="left-pane")
        vs.border_title = "sidebar"

        yield Header()
        with Container(id="app-grid"):
            with vs:
                yield Static(f"sidebar")
                yield tree
            with Horizontal(id="top-right"):
                yield Static("Top Right")
            # with Container(id="bottom-right"):
            yield DataTable(id="bottom-right")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.border_title = "Data Catalog"
        table.zebra_stripes = True
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

if __name__ == "__main__":
    app = MyApp()
    app.run()