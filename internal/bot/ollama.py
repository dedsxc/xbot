import time

from internal.config import config
from internal.api.ollama_client import OllamaAPI
from internal.api.interact_browser import tweet_with_media


class OllamaBot:
    def __init__(self):
        self.api = OllamaAPI(host=config.get('ollama', 'host'),
                             system_prompt=config.get('ollama', 'system_prompt', fallback=None),
                             model=config.get('ollama', 'model', fallback=None))
        self.user_prompt = config.get('ollama', 'user_prompt', fallback="Hello, how can I assist you today?")
        self.delay = config.getint('ollama', 'delay', fallback=300)

    def run(self):
        while True:
            res = self.api.chat(user_prompt=self.user_prompt)
            tweet_with_media(filename=None, tweet_text=res.message['content'], tweet_comment=None)
            time.sleep(self.delay)