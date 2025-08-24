import os
import time

# API
from internal.api.selenium import tweet_with_media
from internal.api.reddit import RedditScraper

# Common
from common.logger import log
from internal.config import config
from common.common import download_media

# Services
from internal.services.redis import RedisDataManager


class RedditBot:
    def __init__(self):
        self.media_directory = os.path.join(os.getcwd(), 'medias')
        self.screenshot_directory = os.path.join(os.getcwd(), 'screenshot')
        self.delay = config.getint('reddit', 'delay', fallback=300)
        self.allowed_media_extension = ["jpg", "jpeg", "png", "mp4", "gif", "webp"]
        self.hashtag_list = config.get('twitter', 'hashtag_list', fallback='').split(',')
        self.footer_text = config.get('twitter', 'footer_text')

    def run(self, db: RedisDataManager, subreddit_list: list, reddit_client: RedditScraper):
        normalized_subreddit_list = [s.lower().strip() for s in subreddit_list]
        while True:
            for subreddit in normalized_subreddit_list:
                submission = reddit_client.get_latest_post(subreddit)
                try:
                    # Check for reddit submission if it exists
                    if not db.check_data_exist(submission.id):
                        # Insert submission_id on database
                        db.insert_data(submission.id)

                        log.info('[post_from_reddit] New Reddit post title: {}'.format(submission.title))
                        # check if submission content is a video
                        if submission.is_video:
                            filename = submission.media['reddit_video']['fallback_url'].split("/")[-2] + ".mp4"
                            reddit_media_path = self.media_directory + "/" + filename
                            download_media(submission.media['reddit_video']['fallback_url'], reddit_media_path)
                            status = f'{submission.title}\nLink: {submission.shortlink}\n\n{" ".join(f"#{hashtag.strip()}" for hashtag in self.hashtag_list if hashtag.strip())}\n\n{self.footer_text}'
                            tweet_with_media(reddit_media_path, status)
                            os.remove(reddit_media_path)
                        elif submission.url.split(".")[-1] in self.allowed_media_extension:
                            reddit_media_path = self.media_directory + "/" + submission.url.split("/")[-1]
                            download_media(submission.url, reddit_media_path)
                            status = f'{submission.title}\nLink: {submission.shortlink}\n\n{" ".join(f"#{hashtag.strip()}" for hashtag in self.hashtag_list if hashtag.strip())}\n\n{self.footer_text}'
                            tweet_with_media(reddit_media_path, status)
                            os.remove(reddit_media_path)

                        elif hasattr(submission, "is_gallery") and submission.is_gallery:
                            media_metadata = getattr(submission, "media_metadata", {})
                            if media_metadata:
                                medias_path = []
                                for idx, (media_id, media_info) in enumerate(media_metadata.items()):
                                    # Limit to 4 media items
                                    if idx >= 4:
                                        break
                                    media_url = media_info["s"]["u"].replace("&amp;", "&")
                                    file_ext = media_url.split(".")[-1].split("?")[0]
                                    reddit_media_path = os.path.join(self.media_directory, f"{media_id}.{file_ext}")
                                    download_media(media_url, reddit_media_path)
                                    medias_path.append(reddit_media_path)

                                # Post tweet with all media files
                                status = f'{submission.title}\nLink: {submission.shortlink}\n\n{" ".join(f"#{hashtag.strip()}" for hashtag in self.hashtag_list if hashtag.strip())}\n\n{self.footer_text}'
                                tweet_with_media(medias_path, status)
                                # Remove downloaded media files
                                for media_path in medias_path:
                                    os.remove(media_path)
                            else:
                                log.warning("[post_from_reddit] No media metadata found for gallery post.")
                        else:
                            log.warning("[post_from_reddit] no media found: {}".format(submission.url))
                            log.warning("[post_from_reddit] url post: {}".format(submission.shortlink))

                except Exception as e:
                    log.error("[post_from_reddit] Error while posting tweet: {}".format(e))
            time.sleep(self.delay)

