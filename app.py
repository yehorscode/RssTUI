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
        
        yield Button("Add a feed", classes="add-feed", id="add-feed")
        yield Button("Manage feeds", classes="manage-feeds", id="manage-feeds")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id and button_id.startswith("feed-"):
            feed_index = int(button_id.split("-")[1])
            feed_title = self.feed_titles[feed_index]
            self.post_message(self.FeedSelected(feed_index, feed_title))


class FeedDisplay(VerticalScroll):
    selected_feed = reactive(0)
    selected_feed_title = reactive("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feed = None
        self.showing_article = False

    def compose(self) -> ComposeResult:
        yield Static("This is RssTUI", classes="feed-content")

    def update_feed(self, feed_index: int, feed_title: str) -> None:
        self.selected_feed = feed_index
        self.selected_feed_title = feed_title
        self.showing_article = False

        self._clear_all_dynamic_content()
        self.call_after_refresh(self._load_feed_content, feed_title)

    def _load_feed_content(self, feed_title: str) -> None:
        content_widget = self.query_one(".feed-content", Static)
        content_widget.update(f"Feed is {feed_title}. Click on any article 2 open it!")

        try:
            self.feed = get_feed_json(feed_title)
            if "entries" in self.feed:
                self._show_article_list()
        except Exception as e:
            self.mount(
                Static(
                    f"Well, well, well... WHat do we have here: {e}", classes="error"
                )
            )

    def _clear_all_dynamic_content(self) -> None:
        widgets_to_remove = []

        for child in self.children:
            if hasattr(child, "id") and child.id:
                if (
                    child.id.startswith("article-button-")
                    or child.id == "back-button"
                    or hasattr(child, "classes")
                    and any(
                        cls in child.classes
                        for cls in ["article-content", "article-title", "error"]
                    )
                ):
                    widgets_to_remove.append(child)

        for widget in widgets_to_remove:
            try:
                widget.remove()
            except Exception:
                pass

    def _show_article_list(self) -> None:
        self.showing_article = False
        for i, entry in enumerate(self.feed["entries"]):
            if "title" in entry:
                self.mount(
                    Button(
                        entry["title"],
                        id=f"article-button-{i}",
                        classes="title-button",
                    )
                )

    def _show_article(self, article_index: int) -> None:
        self.showing_article = True
        self._clear_all_dynamic_content()

        article = self.feed["entries"][article_index]
        self.mount(Button("Take me back", id="back-button", classes="back-button"))
        self.mount(Static(article["title"], classes="article-title", id="article-title"))
        self.mount(Static(article["summary"], classes="article-content", id="article-content"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id and button_id.startswith("article-button"):
            article_index = int(button_id.split("-")[-1])
            self._show_article(article_index)
        elif button_id == "back-button":
            self._clear_all_dynamic_content()
            self.call_after_refresh(self._show_article_list)


class RssTUI(App):

    CSS_PATH = "styles/app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="❀", id="header")
        yield Horizontal(
            Sidebar(id="sidebar"),
            FeedDisplay(id="main-area"),
        )
        yield Footer(show_command_palette=False, id="footer")

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
