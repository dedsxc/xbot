import os
import time

# API
from internal.api.selenium import tweet_with_media
from internal.api.lemmy import LemmyScraper

# Common
from common.logger import log
from internal.config import config
from common.common import download_media

# Services
from internal.services.redis import RedisDataManager


class LemmyBot:
    def __init__(self):
        self.media_directory = os.path.join(os.getcwd(), 'medias')
        self.screenshot_directory = os.path.join(os.getcwd(), 'screenshot')
        self.delay = config.getint('lemmy', 'delay', fallback=300)
        self.allowed_media_extension = ["jpg", "jpeg", "png", "mp4", "gif", "webp"]
        self.hashtag_list = config.get('twitter', 'hashtag_list', fallback='').split(',')
        self.footer_text = config.get('twitter', 'footer_text')

    def run(self, db: RedisDataManager, community_name):
        # Initialize Lemmy API client
        lemmyapi = LemmyScraper()
        while True:
            # Get last post from Lemmy r/unixporn
            lemmy_data = lemmyapi.get_latest_posts(limit=1, sort='New', community_name=community_name)
            try:
                # Check for lemmy post if it exists
                if not db.check_data_exist(lemmy_data.post.id):
                    # Insert lemmy_data_id on database
                    db.insert_data(lemmy_data.post.id)

                    log.info('[post_from_lemmy] New Lemmy post title: {}'.format(lemmy_data.post.name))
                    print(lemmy_data.post.url)
                    if lemmy_data.post.url.split(".")[-1] in self.allowed_media_extension:
                        lemmy_media_path = self.media_directory + "/" + lemmy_data.post.url.split("/")[-1]
                        download_media(lemmy_data.post.url, lemmy_media_path)
                        status = f'{lemmy_data.post.name}\nLink: {lemmy_data.post.ap_id}\n\n{" ".join(f"#{hashtag.strip()}" for hashtag in self.hashtag_list if hashtag.strip())}\n\n{self.footer_text}'
                        tweet_with_media(lemmy_media_path, status)
                        os.remove(lemmy_media_path)
                    else:
                        log.warning("[post_from_lemmy] no media found: {}".format(lemmy_data.post.url))
                        log.warning("[post_from_lemmy] url post: {}".format(lemmy_data.post.ap_id))
            except Exception as e:
                log.error("[post_from_lemmy] Error while posting tweet: {}".format(e))
            time.sleep(self.delay)

    
