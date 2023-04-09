from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False)
    about_me = db.Column(db.String(80), nullable=True)
    private = db.Column(db.Boolean, nullable=False)

    # Business
    is_business = db.Column(db.Boolean, nullable=False)
    address = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.String(80), nullable=True)
    zip_code = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(80), nullable=True)
    website = db.Column(db.String(80), nullable=True)

# Post Model
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref='users', lazy=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    # comments need to be implemented

# Likes Model
class UserLikes(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, primary_key=True)
    like_type = db.Column(db.Integer, nullable=False)

# Rating Model
class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.SmallInteger, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # user = db.relationship('User', backref='users', lazy=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    # post = db.relationship('Post', backref='post_id', lazy=True)

    def __init__(self, rating, business_id, post_id):
        self.rating = rating
        self.business_id = business_id
        self.post_id = post_id

    def __repr__(self):
        return f'{self.rating}-star rating created for {self.business_id} by {self.post_id}'