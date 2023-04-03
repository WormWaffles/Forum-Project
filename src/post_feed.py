from src.models import db, Post

class PostFeed:

    def get_all_posts(self):
        '''Returns all posts'''
        return Post.query.all()
    
    def get_post_by_id(self, post_id):
        '''Returns post by id'''
        return Post.query.get(post_id)
    
    def create_post(self, user_id, title, content, file, likes):
        '''Creates a post'''
        post = Post(user_id=user_id, title=title, content=content, file=file, likes=likes)
        # self.set_file(post.post_id, file)
        db.session.add(post)
        db.session.commit()
        return post
    
    def set_file(self, post_id, file):
        '''Sets the file for a post'''
        # TODO: implement
        pass
    
    def update_post(self, post_id, title, content, file):
        '''Updates a post'''
        post = self.get_post_by_id(post_id)
        post.title = title
        post.content = content
        self.set_file(post_id, file)
        db.session.commit()
        return post
    
    def delete_post(self, post_id):
        '''Deletes a post'''
        post = self.get_post_by_id(post_id)
        db.session.delete(post)
        db.session.commit()
        return post
    
    def like_post(self, post_id, user_id):
        '''Likes a post'''
        # This needs to increment the likes column in the post table, but also add the user_id to the likes table
        # TODO: implement
        pass

    def clear(self):
        '''Clears all posts'''
        Post.query.delete()
        db.session.commit()

post_feed = PostFeed()