from flask import Flask, render_template, redirect, request

app = Flask(__name__)

posts = {}

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

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
    posts[title] = {'content': content}
    print(posts)
    return redirect('/')