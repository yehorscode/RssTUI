import feedparser as fp
import json

with open("feeds.json", "r") as f:
    feeds = json.load(f)

def get_feed_stepone(feed: str):
    return fp.parse(feeds[feed])

def get_feed_json(feed: str):
    feed_data = get_feed_stepone(feed)
    news_feed_json = json.dumps(feed_data, indent=4, default=str)
    with open(f"feed.json", "w") as f:
        f.write(news_feed_json)
    return feed_data  

def get_feed(feed: str):
    return get_feed_json("onion")

