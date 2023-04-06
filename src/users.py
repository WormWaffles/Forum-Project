from src.models import db, User

class Users:

    def get_all_users(self):
        '''Returns all users'''
        return User.query.all()
    
    def get_user_by_id(self, user_id):
        '''Returns user by id'''
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        '''Returns user by username'''
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        '''Returns user by email'''
        return User.query.filter_by(email=email).first()
    
    def create_user(self, username, password):
        '''Creates a user'''
        user = User(username=username, password=password, private=False)
        db.session.add(user)
        db.session.commit()
        return user
    
    def save_profile_pic(self, user_id, profile_pic):
        '''Saves profile pic'''
        # TODO: implement
        pass

    def save_banner_pic(self, banner_pic, user_id):
        '''Saves banner pic'''
        # TODO: implement
        pass

    def update_user(self, user_id, username, password, first_name, last_name, email, about_me, profile_pic, banner_pic, private):
        '''Updates a user'''
        user = self.get_user_by_id(user_id)
        user.username = username
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.about_me = about_me
        self.save_profile_pic(user.user_id, profile_pic)
        self.save_banner_pic(banner_pic, user.user_id)
        if private == '1':
            user.private = True
        else:
            user.private = False
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