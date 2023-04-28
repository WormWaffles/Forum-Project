from src.models import db, User, Post
import uuid
from sqlalchemy import text


class Users:

    def get_all_users(self):
        '''Returns all users'''
        return User.query.all()
    
    def get_all_businesses(self):
        '''Returns all businesses'''
        return User.query.filter_by(is_business=True).all()
    
    def get_user_by_id(self, user_id):
        '''Returns user by id'''
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        '''Returns user by username'''
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        '''Returns user by email'''
        return User.query.filter_by(email=email).first()
    
    def get_business_by_location(self, location):
        '''Returns business by location'''
        if not location:
            return []
        location = location.split(',')
        startlat = float(location[0])
        startlng = float(location[1])
        # get 15 post ordered by closest location, post have location column that is string of "lat,lng"
        posts = db.session.execute(text(f"""
            SELECT
                p.*,
                u.*,
                distance
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
            WHERE subquery.distance < 25 AND u.is_business = true
            ORDER BY subquery.distance
            LIMIT 1;
        """))
        for post in posts:
            post_object = Post(post_id=post[0], user_id=post[1], title=post[2], content=post[3], file=post[4], post_date=post[5], likes=post[6], event=post[7], from_date=post[8], to_date=post[9], location=post[10], comments=post[11], check_in=post[12], user=User(user_id=post[13], username=post[14], password=post[15], first_name=post[16], last_name=post[17], email=post[18], about_me=post[19], location=post[20], private=post[21], profile_pic=post[22], banner_pic=post[23], is_business=post[24], address=post[25], city=post[26], state=post[27], zip_code=post[28], phone=post[29], website=post[30]))
            post_object.distance = post[31]
        print(post_object.user)
        return post_object.user
    
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

    def update_user(self, user_id, username, password, email, about_me, private, profile_pic, banner_pic, is_business=None, address=None, city=None, state=None, zip_code=None, phone=None, website=None,first_name=None, last_name=None):
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
    
    def update_location(self, user_id, lat, lng):
        '''Updates a user's location'''
        user = self.get_user_by_id(user_id)
        user.location = f'{lat},{lng}'
        db.session.commit()
        return user
    
    def search_user(self, search):
        '''Query user names and emails ignore case'''
        user = User.query.filter(User.username.ilike(f'%{search}%')).first()
        if user:
            return user
        return None
    
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