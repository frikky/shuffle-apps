import asyncio
import json
import socket
import time

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from walkoff_app_sdk.app_base import AppBase

class Vader(AppBase):
    __version__ = "1.0.0"
    app_name = "VADER"    # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.headers = {"Content-Type": "application/json"}
        super().__init__(redis, logger, console_logger)


    def sentimentAnalysis(self, text):



        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(text)
        print(str(vs))

        """
        Returns log of what was archived
        """
        message = f"Text {text} analyzed by VADER with a score of " + str(vs)

        # This logs to the docker logs
        self.logger.info(message)
        return str(vs)

if __name__ == "__main__":
    Vader.run()
