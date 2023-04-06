from flask import Flask, render_template, redirect, request, session, g, url_for
from src.post_feed import post_feed # NOTE: we have these two new variables
from src.users import users
from src.likes import likes
from src.models import db, User
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)

# Database Connection
load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] \
    = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# I don't know what this does
app.secret_key='SecretKey'
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# this can be put somewhere else i think
def logged_in():
    '''Checks if user is logged in'''
    if 'user_id' in session:
        return True
    else:
        return False


@app.before_request
def before_request():
    '''Checks if user is logged in'''
    # post_feed.clear()
    # likes.clear()
    g.user = None
    if 'user_id' in session:
        user = users.get_user_by_id(session['user_id'])
        if user == None:
            session.pop('user_id', None)
        else:
            g.user = user


@app.route('/')
def index():
    return render_template('index.html', logged_in=logged_in(), home="active", user=g.user, posts=post_feed.get_all_posts_ordered_by_likes(), likes=likes.get_all_likes())


@app.route('/feed')
def feed():
    return render_template('feed.html', logged_in=logged_in(), feed="active", user=g.user, posts=post_feed.get_all_posts_ordered_by_date(), likes=likes.get_all_likes())


# account page
@app.route('/account')
def account():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('account.html', account="active", user=g.user)

@app.route('/account/edit')
def edit_account():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('settings.html', account="active", user=g.user)

@app.route('/account/edit', methods=['POST'])
def edit_account_post():
    if not g.user:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    about_me = request.form['about_me']
    profile_pic = request.files['profile_pic']
    banner_pic = request.files['banner_pic']
    private = request.form.get('private')

    # needs more error handling
    if password != "":
        message = ""
        unsaved_user = User(user_id=user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, about_me=about_me, profile_pic=profile_pic, banner_pic=banner_pic, private=private)
        if password != confirm_password:
            message = 'Passwords do not match.'
            return render_template('settings.html', user=unsaved_user, message=message, logged_in=logged_in(), account="active")
        if len(password) < 6:
            message = 'Password must be at least 6 characters.'
            return render_template('settings.html', user=unsaved_user, message=message, logged_in=logged_in(), account="active")
    else:
        password = g.user.password
    users.update_user(user_id, username, password, first_name, last_name, email, about_me, profile_pic, banner_pic, private)
    
    return redirect(url_for('account'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    info = {}
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username']
        password = request.form['password']
        user = users.get_user_by_username(username)
        if user and user.password == password:
            session['user_id'] = user.user_id
            return redirect(url_for('account'))
        else:
            message = f"Username or password incorrect. Click here to "
            return render_template('login.html', message=message, logged_in=logged_in(), login="active")
    return render_template('login.html', logged_in=logged_in(), login="active", info=info)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    info = {}
    if request.method == 'POST':
        global logged_in
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        info = {'username': username, 'email': email, 'password': password, 'confirm_password': confirm_password}
        
        if username != "" and email != "" and password != "" and confirm_password != "":
            if not (re.fullmatch(regex, email)):
                message = 'Email is not valid.'
                return render_template('register.html', message=message, logged_in=logged_in(), register="active", username=username, info=info)
            if password != confirm_password:
                message = 'Passwords do not match.'
                return render_template('register.html', message=message, logged_in=logged_in(), register="active", username=username, info=info)
            if len(password) < 6:
                message = 'Password must be at least 6 characters.'
                return render_template('register.html', message=message, logged_in=logged_in(), register="active", username=username, info=info)
            
            existing_user = users.get_user_by_username(username)
            if existing_user:
                message = 'Username already exists.'
                return render_template('register.html', message=message, logged_in=logged_in(), register="active", username=username, info=info)
            
            existing_email = users.get_user_by_email(email)
            if existing_email:
                message = 'email'
                return render_template('register.html', message=message, logged_in=logged_in(), register="active", username=username, info=info)
        
        new_user = users.create_user(username, password)
        session['user_id'] = new_user.user_id

        return redirect(url_for('account'))
    
    return render_template('register.html', logged_in=logged_in(), register="active", info=info)


# create post
@app.route('/create')
def create():
    return render_template('create.html', user=g.user)

@app.post('/feed/post')
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    if not file:
        file = ""
    # get user id
    user_id = session['user_id']
    post_feed.create_post(user_id, title, content, file, 0)
    return redirect('/feed')

# delete post
@app.post('/feed/delete/<post_id>')
def delete_post(post_id):
    if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
        return redirect('/error')
    post_feed.delete_post(post_id)
    return redirect('/feed')


# like post
@app.get('/feed/like/<int:post_id>')
def like_post(post_id):
    user_id = session['user_id']
    post_feed.like_post(post_id, user_id)
    return "nothing"

# dislike post
@app.get('/feed/dislike/<int:post_id>')
def dislike_post(post_id):
    user_id = session['user_id']
    post_feed.dislike_post(post_id, user_id)
    return "nothing"

# remove like or dislike
@app.get('/feed/remove_like/<int:post_id>')
def remove_like(post_id):
    user_id = session['user_id']
    post_feed.remove_like(post_id, user_id)
    return "nothing"

# edit post
@app.get('/feed/edit/<post_id>')
def edit(post_id):
    if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
        return redirect('/error')
    return render_template('edit.html', post=post_feed.get_post_by_id(post_id), user=g.user)

@app.post('/feed/edit/<post_id>')
def edit_post(post_id):
    if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
        return redirect('/error')
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    if not file:
        file = ""
    post_feed.update_post(post_id, title, content, file)
    return redirect('/feed')


#  view post
@app.get('/feed/<post_id>')
def view_post(post_id):
    return render_template('view_post.html', post=post_feed.get_post_by_id(post_id), user=g.user, like=likes.get_like_by_user_id_and_post_id(session['user_id'], post_id))

# view user
@app.get('/user/<user_id>')
def view_user(user_id):
    if int(g.user.user_id) == int(user_id):
        return redirect('/account')
    return render_template('view_user.html', user=users.get_user_by_id(user_id), posts=post_feed.get_posts_by_user_id(user_id), logged_in=logged_in())


# error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', logged_in=logged_in(), e=e, user=g.user), 404