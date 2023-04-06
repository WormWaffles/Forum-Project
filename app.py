from flask import Flask, render_template, redirect, request, session, g, url_for
from src.post_feed import post_feed # NOTE: we have these two new variables
from src.users import users
from src.business import business_users
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
    elif 'business_id' in session:
        return True
    else:
        return False


@app.before_request
def before_request():
    '''Checks if user is logged in'''
    # post_feed.clear()
    # likes.clear()
    g.user = None
    g.business = None
    if 'user_id' in session:
        user = users.get_user_by_id(session['user_id'])
        if user == None:
            session.pop('user_id', None)
        else:
            g.user = user
    elif 'business_id' in session:
        business = business_users.get_business_by_id(session['business_id'])
        if business == None:
            session.pop('business_id', None)
        else:
            g.business = business


@app.route('/')
def index():
    if g.business:
        return render_template('index.html', logged_in=logged_in(), home="active", user_id=g.business.business_id, business=g.business, user=None, posts=post_feed.get_all_posts_ordered_by_likes(), likes=likes.get_all_likes())
    elif g.user:
        return render_template('index.html', logged_in=logged_in(), home="active", user_id=g.user.user_id, user=g.user, posts=post_feed.get_all_posts_ordered_by_likes(), likes=likes.get_all_likes())
    return render_template('index.html', logged_in=logged_in(), home="active")


@app.route('/feed')
def feed():
    if g.business:
        return render_template('feed.html', logged_in=logged_in(), feed="active", user_id=g.business.business_id, business=g.business, user=None, posts=post_feed.get_all_posts_ordered_by_date(), likes=likes.get_all_likes())
    return render_template('feed.html', logged_in=logged_in(), feed="active", user_id=g.user.user_id, user=g.user, posts=post_feed.get_all_posts_ordered_by_date(), likes=likes.get_all_likes())


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
        email = request.form['email']
        password = request.form['password']
        user = users.get_user_by_email(email)
        bus = business_users.get_business_by_email(email)
        if user and user.password == password:
            session['user_id'] = user.user_id
            return redirect(url_for('account'))
        elif bus and bus.password == password:
            session['business_id'] = bus.business_id
            return redirect(url_for('business_account'))
        else:
            message = f"Username or password incorrect."
            return render_template('login.html', message=message, logged_in=logged_in(), login="active", info=info)
    return render_template('login.html', logged_in=logged_in(), login="active", info=info)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    elif 'business_id' in session:
        session.pop('business_id', None)
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
        
        new_user = users.create_user(username, email, password)
        session['user_id'] = new_user.user_id

        return redirect(url_for('account'))
    
    return render_template('register.html', logged_in=logged_in(), register="active", info=info)


# create post
@app.route('/create')
def create():
    if g.user:
        return render_template('create.html', user=g.user)
    elif g.business:
        return render_template('create.html', business=g.business)
    return redirect('/login')

@app.post('/feed/post')
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    if not file:
        file = ""
    # get user id
    if g.user:
        user_id = session['user_id']
    elif g.business:
        user_id = session['business_id']
    else:
        return redirect('/error')
    post_feed.create_post(user_id, title, content, 0)
    return redirect('/feed')

# delete post
@app.get('/feed/delete/<post_id>')
def delete_post(post_id):
    if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
        return redirect('/error')
    post_feed.delete_post(post_id)
    return redirect('/feed')


# like post
@app.get('/feed/like/<int:post_id>')
def like_post(post_id):
    if g.user:
        user_id = session['user_id']
    elif g.business:
        user_id = session['business_id']
    else:
        return redirect('/error')
    post_feed.like_post(post_id, user_id)
    return "nothing"

# dislike post
@app.get('/feed/dislike/<int:post_id>')
def dislike_post(post_id):
    if g.user:
        user_id = session['user_id']
    elif g.business:
        user_id = session['business_id']
    else:
        return redirect('/error')
    post_feed.dislike_post(post_id, user_id)
    return "nothing"

# remove like or dislike
@app.get('/feed/remove_like/<int:post_id>')
def remove_like(post_id):
    if g.user:
        user_id = session['user_id']
    elif g.business:
        user_id = session['business_id']
    else:
        return redirect('/error')
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
    if isinstance(post_id, int):
        return render_template('view_post.html', post=post_feed.get_post_by_id(post_id), user=g.user, likes=likes.get_like_by_post_id(post_id))
    return redirect('/error')

# view user
@app.get('/user/<user_id>')
def view_user(user_id):
    if int(g.user.user_id) == int(user_id):
        return redirect('/account')
    return render_template('view_user.html', user=users.get_user_by_id(user_id), posts=post_feed.get_posts_by_user_id(user_id), logged_in=logged_in())

# buesniess page
# account page for business
@app.route('/business/account')
def business_account():
    if not g.business:
        return redirect(url_for('login'))
    
    return render_template('business_account.html', account="active", business=g.business)

@app.route('/business/register', methods=['GET', 'POST'])
def business():
    info = {}
    if request.method == 'POST':
        global logged_in
        business_name = request.form['business_name']
        business_email = request.form['business_email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        info = {'business_name': business_name, 'business_email': business_email, 'password': password, 'confirm_password': confirm_password}
        
        if business_name != "" and business_email != "" and password != "" and confirm_password != "":
            if not (re.fullmatch(regex, business_email)):
                message = 'Email is not valid.'
                return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
            if password != confirm_password:
                message = 'Passwords do not match.'
                return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
            if len(password) < 6:
                message = 'Password must be at least 6 characters.'
                return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
            
            existing_user = business_users.get_business_by_name(business_name)
            if existing_user:
                message = 'Username already exists.'
                return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
            
            existing_email = business_users.get_business_by_email(business_email)
            if existing_email:
                message = 'email'
                return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        
        new_user = business_users.create_business(business_name, business_email, password)
        session['business_id'] = new_user.business_id

        return redirect(url_for('business_account'))
    
    return render_template('business_register.html', logged_in=logged_in(), register="active", info=info)


# error page
@app.errorhandler(404)
def page_not_found(e):
    if g.business:
        return render_template('error.html', logged_in=logged_in(), e=e, business=g.business, user=None), 404
    return render_template('error.html', logged_in=logged_in(), e=e, user=g.user, business=None), 404