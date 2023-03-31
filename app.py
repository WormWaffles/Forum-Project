from flask import Flask, render_template, redirect, request, session, g, url_for
import random
from src.post_feed import post_feed # NOTE: we have these two new variables
from src.users import users
from src.models import db
from dotenv import load_dotenv
import os

app = Flask(__name__)

# load database
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
# app.secret_key='SecretKey'


# @app.before_request
# def before_request():
#     g.user = None

#     if 'user_id' in session:
#         user = [x for x in users if x.id == session ['user_id']]
#         g.user = user
#         if len(user) >0:
#             g.user =user[0]

@app.route('/')
def index():
    new_user = users.create_user('admin', 'admin')
    new_post = post_feed.create_post(1, 'Title', 'Content', 'File', 0)
    return render_template('index.html', post=new_post, user=new_user)

# @app.route('/feed')
# def feed():
#     return render_template('feed.html', posts=my_feed.get_all_posts(), logged_in=logged_in, feed="active")


# # go to create post page
# @app.route('/create')
# def create():
#     return render_template('create.html')


# @app.get('/login')
# def login_nav():
#     return render_template('login.html', logged_in=logged_in, login="active")


# @app.post('/login')
# def login():
#     session.pop('user_id',None)
#     username = request.form['username']
#     password = request.form['password']
#     user = [x for x in users if x.username == username]
#     if user and user[0].password == password:
#         session['user_id'] = user[0].id
#         global logged_in
#         logged_in = True
#         return redirect(url_for('account', account="active"))
#     else:
#         message = f"Username or password incorrect. Click here to "
#         return render_template('login.html', message=message, logged_in=logged_in, login="active")

# @app.route('/account')
# def account():
#     if not g.user:
#         return redirect(url_for('login', login="active"))
    
#     return render_template('account.html', account="active")

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         global logged_in
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
        
#         if password != confirm_password:
#             message = 'Passwords do not match.'
#             return render_template('register.html', message=message, logged_in=logged_in, register="active")
        
#         existing_user = [x for x in users if x.username == username]
#         if existing_user:
#             message = 'Username already exists. Please choose a different username.'
#             return render_template('register.html', message=message, logged_in=logged_in)
        
#         new_user = User(id=random.randint(1000, 9999), username=username, password=password)
#         users.append(new_user)
#         session['user_id'] = new_user.id
#         logged_in = True

#         return redirect(url_for('account', account="active"))
    
#     return render_template('register.html', logged_in=logged_in, register="active")


# # create post
# @app.post('/add_post')
# def add_post():
#     title = request.form.get('title')
#     content = request.form.get('content')
#     file = request.files['file']
#     # get random id
#     post_id = random.randint(1, 100000)
#     my_feed.create_post(post_id, user_id, title, content, file, [], [], [])
#     return redirect('/feed')

# # delete post
# @app.post('/delete_post')
# def delete_post():
#     post_id = int(request.form.get('post_id'))
#     my_feed.delete_post(post_id)
#     return redirect('/feed')

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

# # edit post passthrough
# @app.post('/edit')
# def edit():
#     post_id = int(request.form.get('post_id'))
#     return render_template('edit.html', posts=my_feed.get_all_posts() ,post_id=post_id)

# # edit post
# @app.post('/edit_post')
# def edit_post():
#     post_id = int(request.form.get('post_id'))
#     title = request.form.get('title')
#     content = request.form.get('content')
#     file = request.files['file']
#     my_feed.update_post(post_id, title, content, file)
#     return redirect('/feed')

# # get error
# @app.get('/error')
# def error():
#     return render_template('error.html')

# # redirect to error.html
# @app.errorhandler(404)
# def page_not_found(e):
#     return redirect('/error')
