from src.models import db, Rating
from sqlalchemy.sql import func

class Ratings:

    def get_all_ratings(self):
        '''Returns all ratings'''
        return Rating.query.all()
    
    def get_rating_average(self, user_id):
        '''Returns average rating'''
        if db.session.query(func.avg(Rating.rating)).filter(Rating.business_id == user_id).scalar() is None:
            average = 0
        else:
            average = round(db.session.query(func.avg(Rating.rating)).filter(Rating.business_id == user_id).scalar())
        return average
    
    def create_rating(self, rating, user_id, post_id):
        '''Creates a rating'''
        rating = Rating(rating=rating, business_id=user_id, post_id=post_id)
        db.session.add(rating)
        db.session.commit()
        return rating
    
    def clear(self):
        '''Clears all ratings'''
        Rating.query.delete()
        db.session.commit()

rating = Ratings()