from flask import Flask, render_template, redirect, request
import random
from src.post_feed import get_feed

app = Flask(__name__)

my_feed = get_feed()
logged_in = True

# sample post
my_feed.create_post(1, 'Title', 'Content', 'File', 0, 0, [])

@app.route('/')
def index():
    return render_template('index.html', posts=my_feed.get_all_posts(), logged_in=logged_in)

@app.route('/feed')
def feed():
    return render_template('feed.html', posts=my_feed.get_all_posts(), logged_in=logged_in)

@app.route('/account')
def account():
    return render_template('account.html')

# go to create post page
@app.get('/create')
def create():
    return render_template('create.html')

@app.get('/login')
def login():
    return render_template('login.html')

# create post
@app.post('/add_post')
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    # get random id
    post_id = random.randint(1, 100000)
    my_feed.create_post(post_id, title, content, file, 0, 0, [])
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
    my_feed.like_post(post_id)
    return redirect('/')

# dislike post
@app.post('/dislike_post')
def dislike_post():
    post_id = int(request.form.get('post_id'))
    my_feed.dislike_post(post_id)
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