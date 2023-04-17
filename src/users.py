from src.models import db, User
import uuid

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
    
    def create_user(self, username, email, password, is_business=False):
        '''Creates a user'''
        # create uuid for user_id
        id = uuid.uuid1()
        id = id.int
        # make the id 12 digits
        id = str(id)
        id = id[:8]
        id = int(id)
        if is_business:
            user = User(user_id=id, username=username, email=email, password=password, private=False, is_business=True)
        else:
            user = User(user_id=id, username=username, email=email, password=password, private=False, is_business=False)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user_id, username, password, first_name, last_name, email, about_me, private, profile_pic, banner_pic, is_business=None, address=None, city=None, state=None, zip_code=None, phone=None, website=None):
        '''Updates a user'''
        user = self.get_user_by_id(user_id)
        user.username = username
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.about_me = about_me
        if private == '1':
            user.private = True
        else:
            user.private = False

        user.profile_pic = profile_pic
        user.banner_pic = banner_pic

        # Business
        if is_business != None:
            user.address = address
            user.city = city
            user.state = state
            user.zip_code = zip_code
            user.phone = phone
            user.website = website

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