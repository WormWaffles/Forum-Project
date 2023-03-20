from random import randint

class Post:
    def __init__(self, post_id, user_id, title, content, file, likes, dislikes, comments) -> None:
        self.post_id = post_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.file = file
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments
        self.post = {'id': self.post_id, 'user_id': self.user_id, 'title': self.title, 'content': self.content, 'file': self.file, 'likes': self.likes, 'dislikes': self.dislikes, 'comments': self.comments}