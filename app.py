from flask import Flask, render_template, redirect, request,session,g,url_for
import random

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

posts: dict[int, dict] = { 200 : {'title': 'Post Title', 'content': 'I really like my dog!', 'file': "", 'likes': 0, 'dislikes': 0, 'comments': {} } }

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session ['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/feed')
def feed():
    return render_template('feed.html', posts=posts)


# go to create post page
@app.get('/create')
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