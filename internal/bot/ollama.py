import time

from internal.config import config
from internal.api.ollama_client import OllamaAPI
from internal.api.selenium import tweet_with_media

from common.logger import log

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
            msg_content = res.message['content']
            log.info(f"[OllamaBot] Response: {msg_content}")
            tweet_with_media(filename=None, tweet_text=msg_content, tweet_comment=None)
            time.sleep(self.delay)