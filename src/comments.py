from src.models import db, Comment
from src.users import users

class CommentFeed:
    
    def get_all_comments(self):
        '''Returns all comments'''
        return Comment.query.all()
    
    def get_comments_by_post_id(self, post_id):
        '''Returns all comments by post id'''
        return Comment.query.filter_by(post_id=post_id).all()
    
    def get_comment_by_id(self, comment_id):
        '''Returns comment by id'''
        return Comment.query.get(comment_id)
    
    def create_comment(self, post_id, user_id, content):
        '''Creates a comment'''
        comment = Comment(post_id=post_id, user_id=user_id, content=content, likes=0)
        db.session.add(comment)
        db.session.commit()
        return comment
    
    def update_comment(self, comment_id, content):
        '''Updates a comment'''
        comment = self.get_comment_by_id(comment_id)
        comment.content = content
        db.session.commit()
        return comment
    
    def delete_comment(self, comment_id):
        '''Deletes a comment'''
        comment = self.get_comment_by_id(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return comment
    
    def search_comments(self, search):
        '''Query comment content and usernames ignore case'''
        user = users.search_user(search)
        user_id = 0
        if user:
            user_id = user.user_id
        return Comment.query.filter((Comment.content.ilike('%' + search + '%')) | (Comment.user_id == user_id)).all()
    
comments = CommentFeed()