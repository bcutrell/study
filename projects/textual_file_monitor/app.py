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
from textual.widgets import Button, Footer, Header, DataTable, TabbedContent, Tab, Static, Tree, RichLog
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.reactive import reactive


ROWS = [
    ("task", "time", "status"),
    ("Write code", "3h", "done"),
    ("Test code", "1h", "done"),
    ("Fix bugs", "2h", "in progress"),
]

class TopRight(Container):

    command = reactive("command")

    def render(self):
        if self.command == "Paul":
            return "Paul is the main character of Dune."
        elif self.command == "Jessica":
            return "Jessica is the mother of Paul."
        else:
            return f"Command: {self.command}"

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

        left_pane = Container(id="left-pane")
        left_pane.border_title = "Sidebar"

        top_right = TopRight(id="top-right") # Container(id="top-right")
        top_right.border_title = "Input"

        bottom_right = Container(id="bottom-right")
        bottom_right.border_title = "Output"

        with Container(id="app-grid"):
            with left_pane:
                yield tree
            with top_right:
                yield RichLog(highlight=True, markup=True)
            with bottom_right:
                yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.border_title = "Data Catalog"
        table.zebra_stripes = True
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def on_tree_node_selected(self, node: dict) -> None:
        text_log = self.query_one(RichLog)
        text_log.write(f"Selected: {node.node}")
        # read data.csv and write it to text_log
        with open("data.csv") as f:
            text_log.write(f.read())

        query = self.query_one(TopRight)
        query.command = node.node
        text_log.write(f"Command: {query.command}")


if __name__ == "__main__":
    app = MyApp()
    app.run()