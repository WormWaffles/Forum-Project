from flask import Flask, render_template, redirect, request, session, g, url_for
from src.post_feed import post_feed # NOTE: we have these two new variables
from src.users import users
from src.models import db
from dotenv import load_dotenv
import os

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

# this can be put somewhere else i think
def logged_in():
    '''Checks if user is logged in'''
    if 'user_id' in session:
        return True
    else:
        return False


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = users.get_user_by_id(session['user_id'])
        g.user = user


@app.route('/')
def index():
    return render_template('index.html', logged_in=logged_in(), home="active", user=g.user)


@app.route('/feed')
def feed():
    return render_template('feed.html', posts=post_feed.get_all_posts(), logged_in=logged_in(), feed="active", user=g.user)


# go to create post page
@app.route('/create')
def create():
    return render_template('create.html')


@app.get('/login')
def login_nav():
    return render_template('login.html', logged_in=logged_in(), login="active")


@app.post('/login')
def login():
    session.pop('user_id',None)
    username = request.form['username']
    password = request.form['password']
    user = users.get_user_by_name(username)
    if user and user.password == password:
        session['user_id'] = user.user_id
        return redirect(url_for('account', account="active"))
    else:
        message = f"Username or password incorrect. Click here to "
        return render_template('login.html', message=message, logged_in=logged_in(), login="active")
    
# logoout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index', logged_in=logged_in(), home="active"))

@app.route('/account')
def account():
    if not g.user:
        return redirect(url_for('login', login="active"))
    
    return render_template('account.html', account="active", user=g.user)

@app.route('/account/edit')
def edit_account():
    if not g.user:
        return redirect(url_for('login', login="active"))
    
    return render_template('settings.html', account="active", user=g.user)

@app.route('/account/edit', methods=['POST'])
def edit_account_post():
    print("edit account post")
    if not g.user:
        return redirect(url_for('login', login="active"))
    
    user_id = session['user_id']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        message = 'Passwords do not match.'
        return render_template('settings.html', message=message, logged_in=logged_in(), account="active")
    users.update_user(user_id, username, password)
    
    return redirect(url_for('account', account="active"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        global logged_in
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            message = 'Passwords do not match.'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active")
        
        existing_user = users.get_user_by_name(username)
        if existing_user:
            message = 'Username already exists. Please choose a different username.'
            return render_template('register.html', message=message, logged_in=logged_in())
        
        new_user = users.create_user(username, password)
        session['user_id'] = new_user.user_id

        return redirect(url_for('account', account="active"))
    
    return render_template('register.html', logged_in=logged_in(), register="active")


# create post
@app.post('/add_post')
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
@app.post('/delete_post')
def delete_post():
    post_id = int(request.form.get('post_id'))
    post_feed.delete_post(post_id)
    return redirect('/feed')

# TODO: add like and dislike functionality [I, Colin, am working on this]
# # like post
# @app.post('/like_post')
# def like_post():
#     post_id = int(request.form.get('post_id'))
#     my_feed.like_post(post_id, user_id)
#     return redirect('/feed')

# # dislike post
# @app.post('/dislike_post')
# def dislike_post():
#     post_id = int(request.form.get('post_id'))
#     my_feed.dislike_post(post_id, user_id)
#     return redirect('/feed')

# like post
@app.get('/feed/like/<int:post_id>')
def like_post(post_id):
    print("like post" + str(post_id))
    # user_id = session['user_id']
    # post_feed.like_post(post_id, user_id)
    return "nothing"

# dislike post
@app.get('/feed/dislike/<int:post_id>')
def dislike_post(post_id):
    print("dislike post" + str(post_id))
    # user_id = session['user_id']
    # post_feed.dislike_post(post_id, user_id)
    return "nothing"

# remove like or dislike
@app.get('/feed/remove_like/<int:post_id>')
def remove_like(post_id):
    print("remove like" + str(post_id))
    # user_id = session['user_id']
    # post_feed.remove_like(post_id, user_id)
    return "nothing"

# edit post passthrough
@app.post('/edit')
def edit():
    post_id = int(request.form.get('post_id'))
    return render_template('edit.html', post=post_feed.get_post_by_id(post_id))

# edit post
@app.post('/edit_post')
def edit_post():
    post_id = int(request.form.get('post_id'))
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    if not file:
        file = ""
    post_feed.update_post(post_id, title, content, file)
    return redirect('/feed')

# get error
@app.get('/error')
def error():
    return render_template('error.html', user=g.user)

# redirect to error.html
@app.errorhandler(404)
def page_not_found(e):
    return redirect('error')
