from flask import Flask, render_template, redirect, request
import random

app = Flask(__name__)

posts: dict[int, dict] = { 200 : {'title': 'Post Title', 'content': 'I really like my dog!', 'file': "", 'likes': 0, 'dislikes': 0, 'comments': {} } }

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/feed')
def feed():
    return render_template('feed.html', posts=posts)

@app.route('/account')
def account():
    return render_template('account.html')

# go to create post page
@app.get('/create')
def create():
    return render_template('create.html')

# create post
@app.post('/add_post')
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files['file']
    # ill do something with the file later **
    # get random id
    post_id = random.randint(1, 100000)
    posts[post_id] = {'title': title, 'content': content, 'file': "", 'likes': 0, 'dislikes': 0, 'comments': {}}
    print(posts)
    return redirect('/')

# like post
@app.post('/like_post')
def like_post():
    post_id = int(request.form.get('post_id'))
    posts[post_id]['likes'] += 1
    return redirect('/')

# dislike post
@app.post('/dislike_post')
def dislike_post():
    post_id = int(request.form.get('post_id'))
    posts[post_id]['dislikes'] += 1
    return redirect('/')