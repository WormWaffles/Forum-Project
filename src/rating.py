from src.models import db, Rating
from src.users import users
from sqlalchemy.sql import func

class Ratings:

    def get_all_ratings(self):
        '''Returns all ratings'''
        return Rating.query.all()
    
    def get_rating_by_post_id(self, post_id):
        '''Returns rating by post id'''
        rating = Rating.query.filter_by(post_id=post_id).scalar()
        if rating == None:
            return 0
        return rating.rating
    
    def get_rating_average(self, user_id):
        '''Returns average rating'''
        if db.session.query(func.avg(Rating.rating)).filter(Rating.business_id == user_id).scalar() is None:
            average = 0
        else:
            average = round(db.session.query(func.avg(Rating.rating)).filter(Rating.business_id == user_id).scalar())
        return average
    
    def create_rating(self, rating, user_id, post_id):
        '''Creates a rating'''
        business = users.get_user_by_id(user_id)
        rating = Rating(rating=rating, business_id=user_id, business_name=business.username, post_id=post_id)
        db.session.add(rating)
        db.session.commit()
        return rating
    
    def delete_rating_by_post_id(self, post_id):
        '''Deletes a rating by post id'''
        Rating.query.filter_by(post_id=post_id).delete()
        db.session.commit()
    
    def clear(self):
        '''Clears all ratings'''
        Rating.query.delete()
        db.session.commit()

rating = Ratings()