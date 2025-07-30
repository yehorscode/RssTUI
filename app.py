from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, Button
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message
from get_feed import get_feed_json
import json


class Sidebar(Vertical):

    class FeedSelected(Message):
        def __init__(self, feed_index: int, feed_title: str) -> None:
            self.feed_index = feed_index
            self.feed_title = feed_title
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feed_buttons = []
        try:
            with open("feeds.json", "r") as f:
                feeds_dict = json.load(f)
                self.feed_titles = list(feeds_dict.keys())
        except FileNotFoundError:
            self.feed_titles = ["No feeds.json found"]

    def compose(self) -> ComposeResult:
        yield Static("RSS Feeds", classes="sidebar-title")
        for i, feed in enumerate(self.feed_titles):
            self.feed_buttons.append(feed)
            yield Button(feed, id=f"feed-{i}", classes="feed")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id and button_id.startswith("feed-"):
            feed_index = int(button_id.split("-")[1])
            feed_title = self.feed_titles[feed_index]
            self.post_message(self.FeedSelected(feed_index, feed_title))


class FeedDisplay(VerticalScroll):
    selected_feed = reactive(0)
    selected_feed_title = reactive("")
    _button_counter = 0  # Add counter to ensure unique IDs

    def compose(self) -> ComposeResult:
        yield Static("Welcome to RssTUI!", id="feed-content")

    def update_feed(self, feed_index: int, feed_title: str) -> None:
        self.selected_feed = feed_index
        self.selected_feed_title = feed_title

        content_widget = self.query_one("#feed-content", Static)
        content_widget.update(f"Feed: {feed_title}")

        for widget in self.query("Button.title-button"):
            widget.remove()

        try:
            feed = get_feed_json(feed_title)
            if "entries" in feed:
                for i, entry in enumerate(feed["entries"]):
                    if "title" in entry:
                        title = entry["title"]
                        self._button_counter += 1
                        self.mount(
                            Button(
                                title, id=f"article-button-{self._button_counter}", classes="title-button"
                            )
                        )
        except (KeyError, FileNotFoundError) as e:
            self.mount(Static(f"Error loading feed: {e}", classes="error"))


class RssTUI(App):

    CSS_PATH = "styles/app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="❀")
        yield Horizontal(
            Sidebar(id="sidebar"),
            FeedDisplay(id="main-area"),
        )
        yield Footer(show_command_palette=False)

    def on_sidebar_feed_selected(self, message: Sidebar.FeedSelected) -> None:
        """Handle feed selection messages"""
        feed_display = self.query_one("#main-area", FeedDisplay)
        feed_display.update_feed(message.feed_index, message.feed_title)

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = RssTUI()
    app.run()
