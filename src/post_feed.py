from src.models import db, Post

class PostFeed:

    def get_all_posts(self):
        return Post.query.all()
    
    def get_post_by_id(self, post_id):
        return Post.query.get(post_id)
    
    def create_post(self, user_id, title, content, file, likes):
        post = Post(user_id=user_id, title=title, content=content, file=file, likes=likes)
        db.session.add(post)
        db.session.commit()
        return post
    
    def update_post(self, post_id, title, content, file):
        post = self.get_post_by_id(post_id)
        post.title = title
        post.content = content
        post.file = file
        db.session.commit()
        return post
    
    def delete_post(self, post_id):
        post = self.get_post_by_id(post_id)
        db.session.delete(post)
        db.session.commit()
        return post
    
    def like_post(self, post_id, user_id):
        # TODO: implement
        pass

    def clear(self):
        Post.query.delete()
        db.session.commit()

post_feed = PostFeed()