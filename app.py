from flask import Flask, render_template, redirect, request,session,g,url_for
import random
from src.post_feed import get_feed

app = Flask(__name__)
app.secret_key='somesecretkeythatonlyiknow'

# User Class
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users=[]
users.append(User(id=1, username='Admin', password='Admin'))
users.append(User(id=2, username='Becca', password='secret'))

my_feed = get_feed()

# sample vars
logged_in = True
user_id = 191
#************

# sample post
my_feed.create_post(1, 191, 'Title', 'Content', 'File', [], [], [])

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session ['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return render_template('index.html', posts=my_feed.get_all_posts(), logged_in=logged_in, user_id=user_id)

@app.route('/feed')
def feed():
    return render_template('feed.html', posts=my_feed.get_all_posts(), logged_in=logged_in)


# go to create post page
@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        session.pop('user_id',None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('account'))
        else:
            message = "Username or password is incorrect, or please register!"
            return render_template('login.html', message=message)
        
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/account')
def account():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('account.html')

# create post
@app.post('/add_post')
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    # get random id
    post_id = random.randint(1, 100000)
    my_feed.create_post(post_id, user_id, title, content, file, [], [], [])
    return redirect('/')

# delete post
@app.post('/delete_post')
def delete_post():
    post_id = int(request.form.get('post_id'))
    my_feed.delete_post(post_id)
    return redirect('/')

# like post
@app.post('/like_post')
def like_post():
    post_id = int(request.form.get('post_id'))
    my_feed.like_post(post_id, user_id)
    return redirect('/')

# dislike post
@app.post('/dislike_post')
def dislike_post():
    post_id = int(request.form.get('post_id'))
    my_feed.dislike_post(post_id, user_id)
    return redirect('/')

# edit post passthrough
@app.post('/edit')
def edit():
    post_id = int(request.form.get('post_id'))
    return render_template('edit.html', posts=my_feed.get_all_posts() ,post_id=post_id)

# edit post
@app.post('/edit_post')
def edit_post():
    post_id = int(request.form.get('post_id'))
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    my_feed.update_post(post_id, title, content, file)
    return redirect('/')