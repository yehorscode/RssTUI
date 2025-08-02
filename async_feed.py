import aiohttp
import asyncio
import feedparser
import json
import aiofiles
from typing import Dict, Any, Optional

class AsyncFeedLoader:
    def __init__(self, timeout: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
    
    async def load_feed(self, url: str) -> Optional[Dict[str, Any]]:
        """Load RSS feed asynchronously"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"HTTP {response.status}: {response.reason}")
                    
                    content = await response.text()
                    loop = asyncio.get_event_loop()
                    feed = await loop.run_in_executor(None, feedparser.parse, content)
                    
                    if feed.bozo and hasattr(feed, 'bozo_exception'):
                        raise Exception(f"Feed parsing error: {feed.bozo_exception}")
                    
                    return feed
                    
        except asyncio.TimeoutError:
            raise Exception("Feed loading timeout")
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {e}")
        except Exception as e:
            raise Exception(f"Failed to load feed: {e}")


class AsyncFileHandler:
    """Async file operations for feeds.json"""
    
    @staticmethod
    async def load_feeds() -> Dict[str, str]:
        """Load feeds from feeds.json asynchronously"""
        try:
            async with aiofiles.open("feeds.json", "r") as f:
                content = await f.read()
                return json.loads(content)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise Exception("Invalid feeds.json format")
    
    @staticmethod
    async def save_feeds(feeds: Dict[str, str]) -> None:
        """Save feeds to feeds.json asynchronously"""
        async with aiofiles.open("feeds.json", "w") as f:
            await f.write(json.dumps(feeds, indent=4))
    
    @staticmethod
    async def load_discover_feeds() -> Dict[str, str]:
        """Load discover feeds asynchronously"""
        try:
            async with aiofiles.open("discover.json", "r") as f:
                content = await f.read()
                return json.loads(content)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise Exception("Invalid discover.json format")
