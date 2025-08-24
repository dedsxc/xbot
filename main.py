import threading
import os

# Common
from internal.config import config
from common.common import dir_exist
from common.logger import log

# Services
from internal.services.redis import RedisDataManager
from internal.api.reddit import RedditScraper

# HTTP Server
from internal.http.server import start_server


def main():
    # Start health check server
    start_server(port=config.getint('global', 'http_port', fallback=8000))
    
    media_directory = os.path.join(os.getcwd(), 'medias')
    screenshot_directory = os.path.join(os.getcwd(), 'screenshot')
    dir_exist(media_directory)
    dir_exist(screenshot_directory)
    
    # Initialize Redis Data Manager
    try:
        db = RedisDataManager(host=config.get('redis', 'host'))
    except Exception as e:
        log.error(f"[main] Error initializing Redis Data Manager: {e}")
        return

    # Start bots based on configuration
    if config.getboolean('text', 'enabled'):
        from internal.bot.text import TextBot
        thread_run_text_bot = threading.Thread(target=TextBot().run)
        thread_run_text_bot.start()
        log.info("[main] Text bot started")
    if config.getboolean('ollama', 'enabled'):
        from internal.bot.ollama import OllamaBot
        thread_run_ollama_bot = threading.Thread(target=OllamaBot().run)
        thread_run_ollama_bot.start()
        log.info("[main] Ollama bot started with model: {}".format(config.get('ollama', 'model')))
    if config.getboolean('lemmy', 'enabled'):
        from internal.bot.lemmy import LemmyBot
        thread_run_lemmy_bot = threading.Thread(target=LemmyBot().run, args=(db, config.get('lemmy', 'community_name')))
        thread_run_lemmy_bot.start()
        log.info("[main] Lemmy bot started with community: {}".format(config.get('lemmy', 'community_name')))
    if config.getboolean('reddit', 'enabled'):
        from internal.bot.reddit import RedditBot
        thread_run_reddit_bot = threading.Thread(target=RedditBot().run, args=(db, 
                                                                               config.get('reddit', 'subreddit_list', fallback='').split(','),
                                                                               RedditScraper(
                                                                                   user_agent=config.get('reddit', 'username'),
                                                                                   client_id=config.get('reddit', 'client_id'),
                                                                                   client_secret=config.get('reddit', 'client_secret'),
                                                                                   username=config.get('reddit', 'username'),
                                                                                   password=config.get('reddit', 'password'),
                                                                                   flair_list=config.get('reddit', 'flair_list').split(',')
                                                                               )
                                                                           ))
        thread_run_reddit_bot.start()
        log.info("[main] Reddit bot started with subreddits: {}".format(config.get('reddit', 'subreddit_list')))

if __name__ == '__main__':
    main()
