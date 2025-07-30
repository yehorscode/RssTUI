from textual.app import App, ComposeResult
from textual.widgets import Header, Static, Button
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

    class ModeSelected(Message):
        def __init__(self, mode: str) -> None:
            # "add" == adding a feed
            # "manage" == managing feeds
            # "weather" == weather for current location
            # "clock" == shows a big ass clock
            self.mode = mode
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
        elif button_id == "add-feed":
            self.post_message(self.ModeSelected("add"))
        elif button_id == "manage-feeds":
            self.post_message(self.ModeSelected("manage"))


class FeedDisplay(VerticalScroll):
    selected_feed = reactive(0)
    selected_feed_title = reactive("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feed = None
        self.showing_article = False

    def compose(self) -> ComposeResult:
        yield Static(
            """
 ██████╗ ███████╗███████╗████████╗██╗   ██╗██╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║   ██║██║
██████╔╝███████╗███████╗   ██║   ██║   ██║██║
██╔══██╗╚════██║╚════██║   ██║   ██║   ██║██║
██║  ██║███████║███████║   ██║   ╚██████╔╝██║
╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝
This is RssTUI! Your app for RSS feeds!
What's an RSS Feed? It's a file, that shows really short snippets of news/content from the site \n
It usually links a quick snippet, authors, and the link! \n
Get started by clicking a button on the sidebar! ← ← ← Here on the left \n
Made for Summer of Making 2025 \n
Styled like a flipper zero because i really want one! (pls vote 4 me :-)""",
            classes="feed-content",
        )
        yield Vertical(id="dynamic-content")

    def update_feed(self, feed_index: int, feed_title: str) -> None:
        self.selected_feed = feed_index
        self.selected_feed_title = feed_title
        self.showing_article = False

        self._load_feed_content(feed_title)

    def _load_feed_content(self, feed_title: str) -> None:
        welcome_widget = self.query_one(".feed-content", Static)
        welcome_widget.display = False

        dynamic_container = self._get_clean_dynamic_container()

        feed_info = Horizontal(
            Static(f"Feed is {feed_title}.", classes="feed-info"),
            Static(
                "Click on any article to open it!",
                classes="feed-instruction",
            ),
            classes="feed-info-container",
        )
        dynamic_container.mount(feed_info)

        articles_container = VerticalScroll(classes="articles-list")
        dynamic_container.mount(articles_container)

        try:
            self.feed = get_feed_json(feed_title)
            if "entries" in self.feed:
                self._show_article_list(articles_container)
        except Exception as e:
            articles_container.mount(
                Static(
                    f"Well, well, well... What do we have here: {e}", classes="error"
                )
            )

    def _get_clean_dynamic_container(self):
        """Get a clean dynamic container, ensuring it's ready for new content"""
        try:
            dynamic_container = self.query_one("#dynamic-content")
            dynamic_container.remove_children()
            return dynamic_container
        except Exception:
            # If dynamic-content doesn't exist, create it
            new_container = Vertical(id="dynamic-content")
            self.mount(new_container)
            return new_container

    def _show_welcome_screen(self) -> None:
        """Show the welcome screen and hide any feed content"""
        welcome_widget = self.query_one(".feed-content", Static)
        welcome_widget.display = True
        self._get_clean_dynamic_container()

    def _show_article_list(self, articles_container=None) -> None:
        self.showing_article = False
        try:
            if articles_container is None:
                articles_container = self.query_one(".articles-list")

            for i, entry in enumerate(self.feed["entries"]):
                if "title" in entry:
                    articles_container.mount(
                        Button(
                            entry["title"],
                            id=f"article-button-{i}",
                            classes="title-button",
                        )
                    )
        except Exception as e:
            print(f"Error showing article list: {e}")
            try:
                safe_container = self._get_clean_dynamic_container()
                safe_container.mount(
                    Static(f"Error loading articles: {e}", classes="error")
                )
            except:
                pass

    def _show_article(self, article_index: int) -> None:
        self.showing_article = True

        dynamic_container = self._get_clean_dynamic_container()

        article = self.feed["entries"][article_index]
        dynamic_container.mount(
            Button("Take me back", id="back-button", classes="back-button")
        )
        dynamic_container.mount(
            Static(article["title"], classes="article-title", id="article-title")
        )
        dynamic_container.mount(
            Static(article["summary"], classes="article-content", id="article-content")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id and button_id.startswith("article-button"):
            article_index = int(button_id.split("-")[-1])
            self._show_article(article_index)
        elif button_id == "back-button":
            if hasattr(self, "selected_feed_title") and self.selected_feed_title:
                self._load_feed_content(self.selected_feed_title)
            else:
                dynamic_container = self._get_clean_dynamic_container()
                self._show_article_list()

class AddFeedDisplay(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Static("Add a feed", classes="add-feed-title")


class RssTUI(App):

    CSS_PATH = "styles/app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="❀", id="header")
        yield Horizontal(
            Sidebar(id="sidebar"),
            FeedDisplay(id="feed-display"),
        )

    def on_sidebar_feed_selected(self, message: Sidebar.FeedSelected) -> None:
        """Handle feed selection messages"""
        horizontal_container = self.query_one(Horizontal)
        
        # Remove any non-FeedDisplay widgets
        for widget_id in ["add-feed-display", "manage-display"]:
            try:
                widget = self.query_one(f"#{widget_id}")
                widget.remove()
            except:
                pass
        
        # Get or create FeedDisplay
        try:
            feed_display = self.query_one("#feed-display")
        except:
            feed_display = FeedDisplay(id="feed-display")
            horizontal_container.mount(feed_display)
        
        feed_display.update_feed(message.feed_index, message.feed_title)

    def on_sidebar_mode_selected(self, message: Sidebar.ModeSelected) -> None:
        """Handle mode selection messages"""
        horizontal_container = self.query_one(Horizontal)
        
        # Remove other widgets first
        for widget_id in ["feed-display", "add-feed-display", "manage-display"]:
            try:
                widget = self.query_one(f"#{widget_id}")
                widget.remove()
            except:
                pass
        
        if message.mode == "add":
            horizontal_container.mount(AddFeedDisplay(id="add-feed-display"))
        elif message.mode == "manage":
            # TODO: Implement proper feed management
            horizontal_container.mount(FeedDisplay(id="manage-display"))

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = RssTUI()
    app.run()
