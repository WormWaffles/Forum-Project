from src.models import db, Post, User
from src.likes import likes
from src.users import users
from src.comments import comments
import uuid
import datetime
from sqlalchemy import text

class PostFeed:

    def get_all_posts(self):
        '''Returns all posts'''
        return Post.query.all()
    
    def get_posts_by_user_id(self, user_id):
        '''Returns all posts by user id'''
        return Post.query.filter_by(user_id=user_id).all()
    
    def get_all_posts_ordered_by_likes(self):
        '''Returns all posts ordered by likes'''
        return Post.query.order_by(Post.likes.desc()).limit(15).all()
    
    def get_all_posts_ordered_by_date(self):
        '''Returns all posts ordered by date'''
        return Post.query.order_by(Post.post_date.desc()).limit(15).all()
    
    def get_all_posts_ordered_by_location(self, location):
        '''Returns all posts ordered by closest location'''
        location = location.split(',')
        startlat = float(location[0])
        startlng = float(location[1])
        # get 15 post ordered by closest location, post have location column that is string of "lat,lng"
        posts = db.session.execute(text(f"""
            SELECT
                p.*,
                u.*
            FROM post p
            JOIN (
                SELECT
                    location,
                    SQRT(
                        POW(69.1 * (CAST(split_part(location, ',', 1) AS double precision) - {startlat}), 2) +
                        POW(69.1 * ({startlng} - CAST(split_part(location, ',', 2) AS double precision)) * COS(CAST(split_part(location, ',', 1) AS double precision) / 57.3), 2)
                    ) AS distance
                FROM post
            ) AS subquery
            ON p.location = subquery.location
            JOIN "user" u ON p.user_id = u.user_id
            WHERE subquery.distance < 1
            ORDER BY subquery.distance
            LIMIT 15;
        """))
        post_objects = []
        for post in posts:
            post_object = Post(post_id=post[0], user_id=post[1], title=post[2], content=post[3], file=post[4], post_date=post[5], likes=post[6], event=post[7], from_date=post[8], to_date=post[9], check_in=post[10], location=post[11], user=User(user_id=post[12], username=post[13], password=post[14], first_name=post[15], last_name=post[16], email=post[17], about_me=post[18], location=post[19], private=post[20], profile_pic=post[21], banner_pic=post[22], is_business=post[23], address=post[24], city=post[25], state=post[26], zip_code=post[27], phone=post[28], website=post[29]))
            post_objects.append(post_object)
        return post_objects

    def get_post_by_id(self, post_id):
        '''Returns post by id'''
        return Post.query.get(post_id)
    
    def create_post(self, user_id, title, content, file, likes, event, from_date, to_date, check_in):
        '''Creates a post'''
        # create uuid for post_id
        id = uuid.uuid1()
        id = id.int
        # make the id 12 digits
        id = str(id)
        id = id[:8]
        id = int(id)
        # get current date
        date = datetime.datetime.now()
        user = users.get_user_by_id(user_id)
        if user.location:
            location = user.location
        post = Post(post_id=id, user_id=user_id, title=title, content=content, file=file, post_date=date, likes=likes, event=event, from_date=from_date, to_date=to_date, location=location, comments=0, check_in=check_in)
        
        db.session.add(post)
        db.session.commit()
        return post
    
    def update_post(self, post_id, title, content, file, event, from_date, to_date, check_in):
        '''Updates a post'''
        post = self.get_post_by_id(post_id)
        post.title = title
        post.content = content
        post.file = file
        post.event = event
        post.from_date = from_date
        post.to_date = to_date
        post.check_in = check_in
        db.session.commit()
        return post
    
    def search_posts(self, search):
        '''Query post titles, content, and usernames ignore case'''
        user = users.search_user(search)
        user_id = 0
        if user:
            user_id = user.user_id
        posts = Post.query.filter(Post.title.ilike(f'%{search}%') | Post.content.ilike(f'%{search}%')).all()
        user_posts = Post.query.filter(Post.user_id == user_id).all()
        all_return_posts = posts + user_posts
        # remove duplicates
        return_posts = []
        for post in all_return_posts:
            if post not in return_posts:
                return_posts.append(post)
        return return_posts

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

    def comment_on_post(self, user_id, post_id, comment, file):
        '''Comments on a post'''
        post = self.get_post_by_id(post_id)
        post.comments += 1
        comments.create_comment(post_id, user_id, comment, file)
        db.session.add(post)
        db.session.commit()

    def delete_comment(self, comment_id):
        '''Deletes a comment'''
        comment = comments.get_comment_by_id(comment_id)
        post = self.get_post_by_id(comment.post_id)
        post.comments -= 1
        comments.delete_comment(comment_id)
        db.session.add(post)
        db.session.commit()

    def clear(self):
        '''Clears all posts'''
        Post.query.delete()
        db.session.commit()

post_feed = PostFeed()