from src.models import db, Post
from src.likes import likes

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
        db.session.add(post)
        db.session.commit()
        return post
    
    def update_post(self, post_id, title, content, file):
        '''Updates a post'''
        post = self.get_post_by_id(post_id)
        post.title = title
        post.content = content
        post.file = file
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
        # get like and post object that we need
        like = likes.get_like_by_user_id_and_post_id(user_id, post_id)
        post = self.get_post_by_id(post_id)
        # if a like already exists
        if like:
            # if the like is a dislike, remove the dislike
            if like.like_type == -1:
                post.likes += 1
                likes.update_like(user_id, post_id, 0)
            elif like.like_type == 0: # if unliked, like the post
                post.likes += 1
                likes.update_like(user_id, post_id, 1)
            else: # if this happens, the user is trying to like a post they already liked (aka inspect element)
                return
        # if a like does not exist, make a new one
        else:
            likes.create_like(user_id, post_id, 1)
            post.likes += 1
        # add and commit everything
        db.session.add(post)
        db.session.commit()

    def dislike_post(self, post_id, user_id):
        '''Dislikes a post'''
        # get the like and post object that we need
        like = likes.get_like_by_user_id_and_post_id(user_id, post_id)
        post = self.get_post_by_id(post_id)
        # if a like already exists
        if like:
            # if the like is a like, remove the like and add a dislike
            if like.like_type == 1:
                post.likes -= 2
            elif like.like_type == 0: # if unliked, dislike the post
                post.likes -= 1
            else: # if this happens, the user is trying to dislike a post they already disliked (aka inspect element)
                return
            likes.update_like(user_id, post_id, -1)
        else: # if a like does not exist, make a new one
            likes.create_like(user_id, post_id, -1)
            post.likes -= 1
        # add and commit everything
        db.session.add(post)
        db.session.commit()

    def remove_like(self, post_id, user_id):
        '''Removes a like or dislike'''
        # get the like object that we need
        like = likes.get_like_by_user_id_and_post_id(user_id, post_id)
        # if a like exists
        if like:
            post = self.get_post_by_id(post_id)
            if like.like_type == 1: # if the like is a like, remove the like
                post.likes -= 1
            elif like.like_type == -1: # if the like is a dislike, remove the dislike
                post.likes += 1
            else:
                return # if this happens, the user is trying to remove a like they don't have (aka inspect element)
            likes.update_like(user_id, post_id, 0)
        else:
            return # if this happens, the user is trying to remove a like they don't have (aka inspect element)
        # add and commit everything
        db.session.add(post)
        db.session.commit()

    def clear(self):
        '''Clears all posts'''
        Post.query.delete()
        db.session.commit()

post_feed = PostFeed()