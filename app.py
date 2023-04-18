import pathlib
from flask import Flask, abort, render_template, redirect, request, session, g, url_for, send_from_directory
import requests
from src.post_feed import post_feed
from src.users import users
from src.likes import likes
from src.rating import rating
from src.user_follow import Follows
from src.models import db, User, Rating
from dotenv import load_dotenv
import os
import re
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol
import boto3
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt


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
app.config['SQLALCHEMY_ECHO'] = False # set to True to see SQL queries
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB max upload size

db.init_app(app)

# vars
app.secret_key = os.getenv('SECRET_KEY')
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
bcrypt = Bcrypt(app)

# Google Auth
GOOGLE_CLIENT_ID = '402126507734-2knh1agkn688s2atb55a5oeu062j89f8.apps.googleusercontent.com'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secret_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid'],
    redirect_uri='http://127.0.0.1:5000/callback'
)

# AWS S3 Connection
aws_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')
s3 = boto3.resource('s3',
aws_access_key_id=aws_id,
aws_secret_access_key=aws_secret)
bucket_name = bucket_name


# Check if user is logged in
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
    # users.clear()
    g.user = None
    if 'user_id' in session:
        user = users.get_user_by_id(session['user_id'])
        if user == None:
            session.pop('user_id', None)
        else:
            g.user = user


@app.route('/')
def index():
    if g.user:
        return render_template('index.html', logged_in=True, home="active", posts=post_feed.get_all_posts_ordered_by_likes(), likes=likes.get_all_likes())
    return render_template('index.html', logged_in=False, home="active")


@app.route('/feed')
def feed():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('index.html', logged_in=True, feed="active", posts=post_feed.get_all_posts_ordered_by_date(), likes=likes.get_all_likes())


# account page
@app.route('/account')
def account():
    star = 0
    if not g.user:
        return redirect(url_for('login'))
    if g.user.is_business:
        star = rating.get_rating_average(g.user.user_id)
    followers_num = Follows.get_followers_num(g.user, g.user.user_id)
    return render_template('account.html', account="active", rating=star,followers_num=followers_num)

#followers page
@app.route('/account/followers')
def account_followers():
    followers = Follows.get_all_followers(g.user.user_id)
    return render_template('followers.html',followers=followers)


@app.route('/account/edit', methods=['GET', 'POST'])
def edit_account():
    if request.method == 'GET':
        if not g.user:
            return redirect(url_for('login'))
        return render_template('settings.html', account="active")
    else:
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

        # upload files
        try:
            # set old profile pic paths
            profile_pic_path = g.user.profile_pic
            banner_pic_path = g.user.banner_pic
            if profile_pic:
                # check if file is an image
                if not profile_pic.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return render_template('settings.html', message='Profile picture must be a .jpg, .jpeg, or .png file.')
                new_profile_filename = f'{user_id}_{secure_filename(profile_pic.filename)}'

                # remove old profile pic from s3
                user = users.get_user_by_id(user_id)
                if user.profile_pic != None:
                    print(g.user.profile_pic.split('/')[-1])
                    s3.Object(bucket_name, g.user.profile_pic.split('/')[-1]).delete()

                # upload new profile pic to s3
                s3.Bucket(bucket_name).upload_fileobj(
                    profile_pic,
                    new_profile_filename
                )

                # add filepath to database
                profile_pic_path = f'https://barhive.s3.amazonaws.com/{new_profile_filename}'
            if banner_pic:
                # check if file is a picture
                if not banner_pic.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return render_template('settings.html', message='Banner picture must be a .jpg, .jpeg, or .png file.')
                new_banner_filename = f'{user_id}_{secure_filename(banner_pic.filename)}'

                # remove old banner pic from s3
                user = users.get_user_by_id(user_id)
                if user.banner_pic != None:
                    print(g.user.banner_pic.split('/')[-1])
                    s3.Object(bucket_name, g.user.banner_pic.split('/')[-1]).delete()

                # upload new banner pic to s3
                s3.Bucket(bucket_name).upload_fileobj(
                    banner_pic,
                    new_banner_filename
                )

                # add filepath to database
                banner_pic_path = f'https://barhive.s3.amazonaws.com/{new_banner_filename}'
        except Exception as e:
            print(f"Error uploading files to s3: " + str(e))

    try:
        # needs more error handling
        if password != "":
            message = ""
            unsaved_user = User(user_id=user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, about_me=about_me, private=private)
            if password != confirm_password:
                message = 'Passwords do not match.'
                return render_template('settings.html', user=unsaved_user, message=message, logged_in=logged_in(), account="active")
            if len(password) < 6:
                message = 'Password must be at least 6 characters.'
                return render_template('settings.html', user=unsaved_user, message=message, logged_in=logged_in(), account="active")
            password = bcrypt.generate_password_hash(password).decode()
        else:
            password = g.user.password
        users.update_user(user_id, username, password, first_name, last_name, email, about_me, private, profile_pic_path, banner_pic_path)
        
        return redirect(url_for('account'))
    except Exception as e: 
        print(e)
        error_message = str(e)
        return render_template('error.html', error_message=error_message)
        


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
    info = {}
    if request.method == 'POST':
        session.pop('user_id',None)
        email = request.form['email']
        password = request.form['password']
        if password is None:
            abort(400)
        user = users.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            return redirect(url_for('account'))
        else:
            message = f"Username or password incorrect."
            return render_template('login.html', message=message, logged_in=logged_in(), login="active", info=info)
    return render_template('login.html', logged_in=logged_in(), login="active", info=info)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('index'))
    info = {}
    if request.method == 'POST':
        global logged_in
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        info = {'username': username, 'email': email, 'password': password, 'confirm_password': confirm_password}
        
        # error handling
        if username == "" or email == "" or password == "" or confirm_password == "":
            message = 'All fields are required.'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active", info=info)
        if not (re.fullmatch(regex, email)):
            message = 'Email is not valid.'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active", info=info)
        if password != confirm_password:
            message = 'Passwords do not match.'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active", info=info)
        if len(password) < 6:
            message = 'Password must be at least 6 characters.'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active", info=info)
        existing_user = users.get_user_by_username(username)
        if existing_user:
            message = 'Username already exists.'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active", info=info)
        existing_email = users.get_user_by_email(email)
        if existing_email:
            message = 'email'
            return render_template('register.html', message=message, logged_in=logged_in(), register="active", info=info)
        
        hashed_password = bcrypt.generate_password_hash(password).decode()
        new_user = users.create_user(username, email, hashed_password)
        session['user_id'] = new_user.user_id

        return redirect(url_for('account'))
    
    return render_template('register.html', logged_in=logged_in(), register="active", info=info)


# create post
@app.route('/create', methods=['GET', 'POST'])
def create():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('create.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files['file']
        if g.user.is_business:
            event = request.form.get('event')
            from_date = request.form.get('from_date')
            to_date = request.form.get('to_date')
            if event == "1":
                event = True
            else:
                event = False
            if event:
                if from_date != None:
                    from_date = from_date.replace(" ", "")
                if to_date != None:
                    to_date = to_date.replace(" ", "")
            else:
                from_date = None
                to_date = None
        else:
            event = None
            from_date = None
            to_date = None
        if title == "":
            abort(400)
        post_path = None
        if file:
            try:
                # make sure file is an image
                if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return render_template('settings.html', message='Image must be a .jpg, .jpeg, or .png file.')
                file_title = title.replace(" ", "_")
                new_post_filename = f'{file_title}_{secure_filename(file.filename)}'

                # upload file to s3
                s3.Bucket(bucket_name).upload_fileobj(
                    file,
                    new_post_filename
                )

                # add filepath to database
                post_path = f'https://barhive.s3.amazonaws.com/{new_post_filename}'
            except Exception as e:
                print(f"Error uploading files to s3: " + str(e))

        # get user id
        user_id = session['user_id']
        post_feed.create_post(user_id, title, content, post_path, 0, event, from_date, to_date)
        return redirect('/feed')
    

# delete post
@app.get('/feed/delete/<post_id>')
def delete_post(post_id):
    if not g.user:
        return redirect(url_for('login'))
    if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
        return redirect('/error')
    post = post_feed.get_post_by_id(post_id)
    if post.file:
        # delete file from s3
        post = post_feed.get_post_by_id(post_id)
        s3.Object(bucket_name, post.file.split('/')[-1]).delete()
    post_feed.delete_post(post_id)
    likes.delete_likes_by_post_id(post_id)
    return redirect('/feed')


# like post
@app.get('/feed/like/<int:post_id>')
def like_post(post_id):
    if g.user:
        user_id = session['user_id']
    else:
        return redirect('/error')
    post_feed.like_post(post_id, user_id)
    return "nothing"

# dislike post
@app.get('/feed/dislike/<int:post_id>')
def dislike_post(post_id):
    if g.user:
        user_id = session['user_id']
    else:
        return redirect('/error')
    post_feed.dislike_post(post_id, user_id)
    return "nothing"

# remove like or dislike
@app.get('/feed/remove_like/<int:post_id>')
def remove_like(post_id):
    if g.user:
        user_id = session['user_id']
    else:
        return redirect('/error')
    post_feed.remove_like(post_id, user_id)
    return "nothing"

# edit post
@app.route('/feed/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
            return redirect('/error')
        return render_template('edit.html', post=post_feed.get_post_by_id(post_id))
    else:
        if g.user.user_id != post_feed.get_post_by_id(post_id).user_id:
            return redirect('/error')
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files['file']
        if g.user.is_business:
            event = request.form.get('event')
            from_date = request.form.get('from_date')
            to_date = request.form.get('to_date')
            if event == "1":
                event = True
            else:
                event = False
            if event:
                if from_date != None:
                    from_date = from_date.replace(" ", "")
                if to_date != None:
                    to_date = to_date.replace(" ", "")
            else:
                from_date = None
                to_date = None
        else:
            from_date = None
            to_date = None
        file_path = None
        if file:
            try:
                s3 = boto3.resource('s3',
                aws_access_key_id='AKIAY5EAJ7XAJ3GQ2AUH',
                aws_secret_access_key='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')
                bucket_name = 'barhive'
                if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return render_template('settings.html', message='Banner picture must be a .jpg, .jpeg, or .png file.')
                new_filename = f'{title}_{secure_filename(file.filename)}'

                # remove old banner pic from s3
                post = post_feed.get_post_by_id(post_id)
                if post.file != None:
                    s3.Object(bucket_name, post.file.split('/')[-1]).delete()

                s3.Bucket(bucket_name).upload_fileobj(
                    file,
                    new_filename
                )

                # add filepath to database
                file_path = f'https://barhive.s3.amazonaws.com/{new_filename}'
            except Exception as e:
                print(f"Error uploading files to s3: " + str(e))

        post_feed.update_post(post_id, title, content, file=file_path, event=event, from_date=from_date, to_date=to_date)
        return redirect('/feed')


#  view post
@app.get('/feed/<post_id>')
def view_post(post_id):
    if not g.user:
        return redirect(url_for('login'))
    post = post_feed.get_post_by_id(post_id)
    if post:
        return render_template('view_post.html', post=post, likes=likes.get_like_by_post_id(post_id))
    return redirect('/error')

# view user
@app.get('/user/<user_id>')
def view_user(user_id):
    if not g.user:
        return redirect(url_for('login'))
    if g.user:
        if int(g.user.user_id) == int(user_id):
            return redirect('/account')
    user = users.get_user_by_id(user_id)
    if user:
        followers_num = Follows.get_followers_num(user, user_id)
        is_Following=Follows.is_Foo_Following_Bar(g.user.user_id,user_id)
        return render_template('account.html', user=user,followers_num=followers_num,user_id=user_id,is_Following=is_Following)
    return redirect('/error')

#view a other users followers
@app.get('/user/<user_id>/followers')
def view_user_followers(user_id):
    followers = Follows.get_all_followers(user_id)
    return render_template('followers.html',followers=followers)

#follow method
@app.route('/follow/<user_id>', methods=['POST'])
def follow(user_id):
    #is_Following = True
    Follows.foo_followed_bar(g.user,g.user.user_id,user_id)
    is_Following = True
    return redirect(url_for('view_user',user_id=user_id,is_Following=is_Following))

#unfollow method
@app.route('/unfollow/<user_id>', methods=['POST'])
def unfollow(user_id):
    #is_Following = False
    Follows.foo_unfollowed_bar(g.user.user_id,user_id)
    is_Following = False
    return redirect(url_for('view_user',user_id=user_id,is_Following=is_Following))

# business page
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
        
        if business_name == "" or business_email == "" or password == "" or confirm_password == "":
            message = 'All fields are required.'
            return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        if not (re.fullmatch(regex, business_email)):
            message = 'Email is not valid.'
            return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        if password != confirm_password:
            message = 'Passwords do not match.'
            return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        if len(password) < 6:
            message = 'Password must be at least 6 characters.'
            return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        
        existing_user = users.get_user_by_username(business_name)
        if existing_user:
            message = 'Username already exists.'
            return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        
        existing_email = users.get_user_by_email(business_email)
        if existing_email:
            message = 'email'
            return render_template('business_register.html', message=message, logged_in=logged_in(), register="active", info=info)
        
        hashed_password = bcrypt.generate_password_hash(password).decode()
        new_user = users.create_user(username=business_name, email=business_email, password=hashed_password, is_business=True)
        session['user_id'] = new_user.user_id

        return redirect(url_for('account'))
    
    return render_template('business_register.html', logged_in=logged_in(), register="active", info=info)


# error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', logged_in=logged_in(), e=e), 404


# ********** GOOGLE LOGIN **********
@app.route('/callback')
def callback():
    print("callback")
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    username = id_info.get("name")
    if '(' and ')' in username:
        usernames = username.split(" ")
        username = usernames[len(usernames) - 1].replace("(", "")
        username = username.replace(")", "")
    
    # check if user exists
    existing_user = users.get_user_by_email(id_info.get("email"))
    if existing_user:
        session['user_id'] = existing_user.user_id
        return redirect(url_for('account'))
    else:
        email = id_info.get("email")
        new_user = users.create_user(username, email, None)
        session['user_id'] = new_user.user_id

    return redirect(url_for('account'))

@app.route('/googlelogin')
def googlelogin():
    try:
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)
    except Exception as e:
        #redirect to error page
        return redirect('/error')
# ********** GOOGLE LOGIN **********
