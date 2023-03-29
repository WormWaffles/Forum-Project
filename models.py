from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref='users', lazy=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    file = db.Column(db.String(80), nullable=True)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Integer, nullable=True)