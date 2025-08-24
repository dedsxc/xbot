from pydantic import BaseModel
from pydantic import RootModel
from typing import Optional
from typing import List

class Post(BaseModel):
    id: int
    name: str
    url: Optional[str]
    body: Optional[str]
    creator_id: int
    community_id: int
    removed: bool
    locked: bool
    published: str
    deleted: bool
    nsfw: bool
    thumbnail_url: Optional[str]
    ap_id: str
    local: bool
    language_id: int
    featured_community: bool
    featured_local: bool
    url_content_type: Optional[str]

class Creator(BaseModel):
    id: int
    name: str
    display_name: Optional[str]
    banned: bool
    published: str
    actor_id: str
    local: bool
    deleted: bool
    bot_account: bool
    instance_id: int

class Community(BaseModel):
    id: int
    name: str
    title: str
    description: Optional[str]
    removed: bool
    published: str
    updated: Optional[str]
    deleted: bool
    nsfw: bool
    actor_id: str
    local: bool
    icon: Optional[str]
    banner: Optional[str]
    hidden: bool
    posting_restricted_to_mods: bool
    instance_id: int
    visibility: str

class ImageDetails(BaseModel):
    link: str
    width: int
    height: int
    content_type: str

class Counts(BaseModel):
    post_id: int
    comments: int
    score: int
    upvotes: int
    downvotes: int
    published: str
    newest_comment_time: Optional[str]

class LemmyPost(BaseModel):
    post: Post
    creator: Creator
    community: Community
    image_details: Optional[ImageDetails]
    creator_banned_from_community: bool
    banned_from_community: bool
    creator_is_moderator: bool
    creator_is_admin: bool
    counts: Counts
    subscribed: str
    saved: bool
    read: bool
    hidden: bool
    creator_blocked: bool
    unread_comments: int

class LemmyPostList(BaseModel):
    posts: List[LemmyPost]