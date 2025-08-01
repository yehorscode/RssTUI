from textual.app import App, ComposeResult
from textual.widgets import Header, Static, Button, Input
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message
from get_feed import get_feed_json
import json

class Sidebar(Vertical):

    feed_data = reactive({})

    class FeedSelected(Message):
        def __init__(self, feed_index: int, feed_title: str) -> None:
            self.feed_index = feed_index
            self.feed_title = feed_title
            super().__init__()

    class ModeSelected(Message):
        def __init__(self, mode: str) -> None:
            # "add" == adding a feed
            # "manage" == managing feeds
            # "discover" == discover feeds
            self.mode = mode
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feed_buttons = []
        self.load_feeds()
    
    def load_feeds(self):
        """Load feeds from feeds.json"""
        try:
            with open("feeds.json", "r") as f:
                feeds_dict = json.load(f)
                self.feed_data = feeds_dict
        except FileNotFoundError:
            self.feed_data = {"No feeds.json found": ""}

    def compose(self) -> ComposeResult:
        yield Static("RSS Feeds", classes="sidebar-title")
        
        for feed in self.feed_data.keys():
            if feed != "No feeds.json found":
                self.feed_buttons.append(feed)
                feed_id = feed.replace(" ", "_").replace("/", "_").replace(".", "_")
                yield Button(feed, id=f"feed-{feed_id}", classes="feed")
            else:
                yield Static(feed, classes="no-feeds-message")

        yield Button("Add feed", classes="add-feed", id="add-feed")
        yield Button("Manage feeds", classes="manage-feeds", id="manage-feeds")
        yield Button("Discover feeds", classes="discover-feeds-btn", id="discover-feeds-btn")
    
    async def watch_feed_data(self, new_data: dict) -> None:
        """Called when feed_data changes - rebuild the feed buttons"""
        try:
            add_button = self.query_one("#add-feed")
        except:
            return
        
        current_feeds = list(self.query(".feed"))
        current_messages = list(self.query(".no-feeds-message"))
        
        for widget in current_feeds + current_messages:
            await widget.remove()
        
        self.feed_buttons.clear()
        
        for feed in new_data.keys():
            if feed != "No feeds.json found":
                self.feed_buttons.append(feed)
                feed_id = feed.replace(" ", "_").replace("/", "_").replace(".", "_")
                button = Button(feed, id=f"feed-{feed_id}", classes="feed")
                self.mount(button, before=add_button)
            else:
                message = Static(feed, classes="no-feeds-message")
                self.mount(message, before=add_button)
    
    def refresh_feeds(self):
        """Refresh the sidebar with updated feeds"""
        try:
            with open("feeds.json", "r") as f:
                feeds_dict = json.load(f)
        except FileNotFoundError:
            feeds_dict = {"No feeds.json found": ""}
        
        self.feed_data = {}
        self.feed_data = feeds_dict

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id and button_id.startswith("feed-"):
            feed_id = button_id[5:] 
            feed_title = None
            for feed in self.feed_data.keys():
                if feed.replace(" ", "_").replace("/", "_").replace(".", "_") == feed_id:
                    feed_title = feed
                    break
            
            if feed_title and feed_title in self.feed_data:
                feed_titles = list(self.feed_data.keys())
                feed_index = feed_titles.index(feed_title)
                self.post_message(self.FeedSelected(feed_index, feed_title))
        elif button_id == "add-feed":
            self.post_message(self.ModeSelected("add"))
        elif button_id == "manage-feeds":
            self.post_message(self.ModeSelected("manage"))
        elif button_id == "discover-feeds-btn":
            self.post_message(self.ModeSelected("discover"))


class MainContent(VerticalScroll):
    """The main father and mother of all the content"""
    
    class FeedsChanged(Message):
        """Message sent when feeds are added or deleted"""
        pass
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_feed_data = None
        self.current_feed_title = None
    
    def compose(self) -> ComposeResult:
        yield Vertical(id="content-container")
    
    def show_welcome(self):
        """Welcome screen"""
        container = self.query_one("#content-container")
        container.remove_children()
        
        welcome_text = Static(
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
        container.mount(welcome_text)
    
    def show_feed(self, feed_title: str):
        """Show feed's content"""
        container = self.query_one("#content-container")
        container.remove_children()
        
        self.current_feed_title = feed_title  # Store for back navigation
        
        feed_info = Horizontal(
            Static(f"Feed is {feed_title}.", classes="feed-info"),
            Static("Click on any article to open it!", classes="feed-instruction"),
            classes="feed-info-container",
        )
        container.mount(feed_info)
        
        articles_container = VerticalScroll(classes="articles-list")
        container.mount(articles_container)
        
        try:
            feed = get_feed_json(feed_title)
            self.current_feed_data = feed
            if "entries" in feed:
                for i, entry in enumerate(feed["entries"]):
                    if "title" in entry:
                        articles_container.mount(
                            Button(entry["title"], id=f"article-button-{i}", classes="title-button")
                        )
        except Exception as e:
            articles_container.mount(Static(f"Error: {e}. Restart the app.", classes="error"))

        


    def show_article(self, article_index: int):
        """Show individual article content"""
        container = self.query_one("#content-container")
        container.remove_children()
        
        if not self.current_feed_data or "entries" not in self.current_feed_data:
            container.mount(Static("No article data available", classes="error"))
            return
            
        entries = self.current_feed_data["entries"]
        if article_index >= len(entries):
            container.mount(Static("Article not found", classes="error"))
            return
            
        entry = entries[article_index]
        
        container.mount(Button("← Back to feed", id="back-to-feed", classes="back-button"))
        
        if "title" in entry:
            container.mount(Static(entry["title"], classes="article-title"))
        
        content = ""
        if "summary" in entry:
            content = entry["summary"]
        elif "description" in entry:
            content = entry["description"]
        elif "content" in entry and entry["content"]:
            if isinstance(entry["content"], list) and len(entry["content"]) > 0:
                content = entry["content"][0].get("value", "")
            else:
                content = str(entry["content"])
        
        if content:
            container.mount(Static(content, classes="article-content"))
        else:
            container.mount(Static("No content available for this article", classes="no-content"))
        
        if "link" in entry:
            container.mount(Static(f"\nSee full article: {entry['link']}", classes="article-link"))

        metadata_parts = []
        if "author" in entry:
            metadata_parts.append(f"\nWritten by: {entry['author']}")
        if "published" in entry:
            metadata_parts.append(f"On {entry['published']}")
        
        if metadata_parts:
            container.mount(Static(" | ".join(metadata_parts), classes="article-metadata"))

    def show_add_feed(self):
        """Add feeds screen"""
        container = self.query_one("#content-container")
        container.remove_children()
        container.mount(Static("Add a feed", classes="add-feed-title"))
        container.mount(Static("""
You can try: (reddit feeds only show titles)
https://www.wired.com/feed/rss
https://www.reddit.com/r/AskReddit/.rss
"""))
        container.mount(Input(placeholder="Name 4 feed", id="feed-name-input", classes="feed-name-input", type="text"))
        container.mount(Input(placeholder="https://onion.com/feed", id="feed-url-input", classes="feed-url-input", type="text"))
        container.mount(Button("Add!", id="add-feed-button", classes="add-feed-button"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """When user submits a new feed or deletes a feed"""
        if event.button.id == "add-feed-button":
            feed_name = self.query_one("#feed-name-input").value
            feed_url = self.query_one("#feed-url-input").value
            
            try:
                with open("feeds.json", "r") as f:
                    feeds_dict = json.load(f)
            except FileNotFoundError:
                feeds_dict = {}
                
            feeds_dict[feed_name] = feed_url
            with open("feeds.json", "w") as f:
                json.dump(feeds_dict, f, indent=4)
            
            self.post_message(self.FeedsChanged())
            self.show_welcome()
        
        elif event.button.id and event.button.id.startswith("article-button-"):
            article_index = int(event.button.id.split("-")[-1])
            self.show_article(article_index)
        
        elif event.button.id == "back-to-feed":
            if self.current_feed_title:
                self.show_feed(self.current_feed_title)
            else:
                self.show_welcome()
        
        elif event.button.id and event.button.id.startswith("manage-delete-feed-"):
            feed_index = int(event.button.id.split("-")[-1])
            
            try:
                with open("feeds.json", "r") as f:
                    feeds_dict = json.load(f)
                
                feed_names = list(feeds_dict.keys())
                if 0 <= feed_index < len(feed_names):
                    feed_to_delete = feed_names[feed_index]
                    del feeds_dict[feed_to_delete]
                    
                    with open("feeds.json", "w") as f:
                        json.dump(feeds_dict, f, indent=4)
                    
                    self.post_message(self.FeedsChanged())
                    
                    self.show_manage_feeds()
                    
            except FileNotFoundError:
                pass
        
        elif event.button.id and event.button.id.startswith("discover-add-feed-"):
            feed_index = int(event.button.id.split("-")[-1])
            
            try:
                with open("discover.json", "r") as f:
                    discover_dict = json.load(f)
                
                with open("feeds.json", "r") as f:
                    feeds_dict = json.load(f)
            except FileNotFoundError:
                feeds_dict = {}
            
            feed_names = list(discover_dict.keys())
            if 0 <= feed_index < len(feed_names):
                feed_name = feed_names[feed_index]
                feed_url = discover_dict[feed_name]
                
                # Add the feed to feeds.json
                feeds_dict[feed_name] = feed_url
                
                with open("feeds.json", "w") as f:
                    json.dump(feeds_dict, f, indent=4)
                
                self.post_message(self.FeedsChanged())
                
                # Stay on discover page to add more feeds if needed
                self.show_discover_feeds()

    def show_manage_feeds(self):
        """Manage feeds screen"""
        container = self.query_one("#content-container")
        container.remove_children()
        container.mount(Static("Manage your feeds", classes="manage-title"))
        
        try:
            with open("feeds.json", "r") as f:
                feeds_dict = json.load(f)
        except FileNotFoundError:
            container.mount(Static("No feeds found. Add some feeds first!", classes="error"))
            return
            
        for i, feed in enumerate(feeds_dict):
            feed_info = Vertical(
                Static(feed, classes="manage-feed-name"),
                Static(feeds_dict[feed], classes="manage-feed-url"),
                classes="manage-feed-info"
            )
            
            delete_button = Button("Delete", id=f"manage-delete-feed-{i}", classes="manage-delete-feed")
            
            container.mount(Horizontal(
                feed_info,
                delete_button,
                classes="manage-feed-row"
            ))

    def show_discover_feeds(self):
        """Discover feeds screen"""
        container = self.query_one("#content-container")
        container.remove_children()
        container.mount(Static("Discover feeds", classes="discover-title"))
        
        try:
            with open("discover.json", "r") as f:
                discover_dict = json.load(f)
        except FileNotFoundError:
            container.mount(Static("No discover.json found. Create one to discover feeds!", classes="error"))
            return
            
        for i, feed in enumerate(discover_dict):
            feed_info = Vertical(
                Static(feed, classes="discover-feed-name"),
                Static(discover_dict[feed], classes="discover-feed-url"),
                classes="discover-feed-info"
            )
            
            add_button = Button(f"Add {feed}!", id=f"discover-add-feed-{i}", classes="discover-add-feed")
            
            container.mount(Horizontal(
                feed_info,
                add_button,
                classes="discover-feed-row"
            ))



class RssTUI(App):

    CSS_PATH = "styles/app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="❀", id="header")
        yield Horizontal(
            Sidebar(id="sidebar"),
            MainContent(id="main-content"),
        )

    def on_mount(self) -> None:
        """Big ass welcome text"""
        main_content = self.query_one("#main-content", MainContent)
        main_content.show_welcome()

    def on_sidebar_feed_selected(self, message: Sidebar.FeedSelected) -> None:
        """Handles messages for feeds"""
        # lmao ts is like scratch
        main_content = self.query_one("#main-content", MainContent)
        main_content.show_feed(message.feed_title)

    def on_sidebar_mode_selected(self, message: Sidebar.ModeSelected) -> None:
        """Handles mode selection (sends messages)"""
        main_content = self.query_one("#main-content", MainContent)
        
        if message.mode == "add":
            main_content.show_add_feed()
        elif message.mode == "manage":
            main_content.show_manage_feeds()
        elif message.mode == "discover":
            main_content.show_discover_feeds()
    
    def on_main_content_feeds_changed(self, message: MainContent.FeedsChanged) -> None:
        """Handle feeds changed message by refreshing the sidebar"""
        sidebar = self.query_one("#sidebar", Sidebar)
        sidebar.refresh_feeds()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = RssTUI()
    app.run()
