import asyncio
import json
import random
import socket
import time

from twython import Twython
from walkoff_app_sdk.app_base import AppBase

class Twitter(AppBase):
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

    def send_tweet(self, consumer_key, consumer_secret, access_token, access_token_secret, message):
        twitter = Twython(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )

        tweet = twitter.update_status(status=message)
        return json.dumps(tweet)

    def delete_tweet(self, consumer_key, consumer_secret, access_token, access_token_secret, tweet_id):
        twitter = Twython(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )

        return twitter.destroy_status(id=tweet_id)

if __name__ == "__main__":
    Twitter.run()
