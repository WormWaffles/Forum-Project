from src.models import db, User

class Users:

    def get_all_users(self):
        return User.query.all()
    
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_user_by_name(self, username):
        return User.query.filter_by(username=username).first()
    
    def create_user(self, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def update_user(self, user_id, username, password):
        user = self.get_user_by_id(user_id)
        user.username = username
        user.password = password
        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return user
    
    def clear(self):
        User.query.delete()
        db.session.commit()

users = Users()