import time

from internal.config import config
from internal.api.selenium import tweet_with_media

from common.logger import log

class TextBot:
    def __init__(self):
        self.message = config.get('text', 'message', fallback="Hello, this is a text-only tweet.")
        self.delay = config.getint('text', 'delay', fallback=300)

    def run(self):
        while True:
            tweet_with_media(filename=None, tweet_text=self.message, tweet_comment=None)
            time.sleep(self.delay)