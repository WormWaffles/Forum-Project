from src.models import db, Follower, User

class Follows:

    #just pay close attention to which user is following which
    def foo_followed_bar(self,follower_user_id,followed_user_id):
        follower = Follower(follower_user_id,followed_user_id)
        db.session.add(follower)
        db.session.commit()
        return follower
    
    def foo_unfollowed_bar(self,follower_user_id,followed_user_id):
        follower = Follower(follower_user_id,followed_user_id)
        db.session.delete(follower)
        db.session.commit()
        return follower
    
    def get_all_followers(self):
        follow_list = User.query.join(Follower, User.user_id==Follower.follower_user_id).add_columns(User.user_id,User.username).filter_by(followed_user_id=self).all()
        return follow_list

    def get_all_following(self,follower_user_id):
        return Follower.query.filter_by(follower_user_id=follower_user_id).all()
    
    def get_followers_num(self,followed_user_id):
        
        num_followers = Follower.query.filter_by(followed_user_id=followed_user_id).count()
        return num_followers
    
    def get_user_by_follower_id(self,follower_user_id):
        return User.query.get(follower_user_id)
    
follows = Follows()