import asyncio
import json
import random
import socket
import time

import feedparser
from walkoff_app_sdk.app_base import AppBase

class PythonPlayground(AppBase):
    __version__ = "1.0.0"
    app_name = "python_playground"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # Write your data inside this function
    def get_rss(self, url):
        # It comes in as a string, so needs to be set to JSON
        NewsFeed = feedparser.parse(url)
        try:
            return json.dumps(NewsFeed)
        except:
            return NewsFeed

        print(NewsFeed)
        return NewsFeed.entries

        print(NewsFeed)
        entry = NewsFeed.entries[1]

        print(entry.keys())
        return entry.keys()

    # Write your data inside this function
    #def get_rss_feed(self, url):
    #    # It comes in as a string, so needs to be set to JSON
    #    NewsFeed = feedparser.parse(url)
    #    NewsFeed.entries[1]
    #
    #    print entry.keys()
    #    return entry.keys()

if __name__ == "__main__":
    PythonPlayground.run()
