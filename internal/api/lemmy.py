import requests
from internal.models.lemmy import LemmyPostList, LemmyPost
from common.logger import log

class LemmyScraper:
    def __init__(self):
        self.base_url = 'https://lemmy.world/api/v3'
        
    def get_latest_posts(self, limit=1, sort='New', community_name='unixporn') -> LemmyPost:
        url = self.base_url + '/post/list'
        params = {
            'community_name': community_name,
            'limit': limit,
            'sort': sort
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            lemmy_data = LemmyPostList.model_validate(data)
            return lemmy_data.posts[0]

        except requests.RequestException as e:
            log.info(f"[get_latest_posts] Error fetching posts: {e}")
            return None