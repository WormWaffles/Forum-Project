from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    about_me = db.Column(db.String(80), nullable=True)
    profile_pic = db.Column(db.String(80), nullable=True)
    banner_pic = db.Column(db.String(80), nullable=True)
    private = db.Column(db.Boolean, nullable=False)

# Post Model
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref='users', lazy=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    file = db.Column(db.String(80), nullable=True)
    likes = db.Column(db.Integer, nullable=False)
    # comments need to be implemented