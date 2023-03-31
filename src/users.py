from src.models import db, User

class Users:

    def get_all_users(self):
        '''Returns all users'''
        return User.query.all()
    
    def get_user_by_id(self, user_id):
        '''Returns user by id'''
        return User.query.get(user_id)
    
    def get_user_by_name(self, username):
        '''Returns user by name'''
        return User.query.filter_by(username=username).first()
    
    def create_user(self, username, password):
        '''Creates a user'''
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def update_user(self, user_id, username, password):
        '''Updates a user'''
        user = self.get_user_by_id(user_id)
        user.username = username
        user.password = password
        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        '''Deletes a user'''
        user = self.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return user
    
    def clear(self):
        '''Clears all users'''
        User.query.delete()
        db.session.commit()

users = Users()