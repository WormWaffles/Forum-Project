from random import randint
from src.post import Post

# Very inspired by Krevet
_my_feed = None

def get_feed():
    global _my_feed

    class PostFeed:
        '''dict of movies [should be entered in database at one point]'''
        def __init__(self):
            self.posts: dict[int, Post] = {}

        def get_all_posts(self):
            return self.posts
        
        def create_post(self, post_id, title, content, file, likes, dislikes, comments) -> Post:
            '''Create new post and add to posts dict'''
            post = Post(post_id, title, content, file, likes, dislikes, comments)
            self.posts[post.post_id] = post

        def update_post(self, post_id, title, content, file) -> Post:
            '''Update existing post'''
            post = self._db.get(post_id)
            if not post:
                raise ValueError(f'movie with id {post_id} not found')
            # update post
            self.posts[post.id] = post
            post.title = title
            post.content = content
            post.file = file
            return post
        
        def delete_post(self, post_id) -> Post:
            '''Delete existing post'''
            post = self._db.get(post_id)
            if not post:
                raise ValueError(f'movie with id {post_id} not found')
            del self.posts[post.id]

        def clear(self) -> None:
            '''Clear all posts'''
            self.posts = {}

    if _my_feed is None:
        _my_feed = PostFeed()

    return _my_feed