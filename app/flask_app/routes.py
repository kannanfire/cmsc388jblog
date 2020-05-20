from flask import render_template, request, redirect, url_for, flash, Response
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from datetime import datetime
import io
import base64

# Local Imports
from . import app, bcrypt
from .forms import (RegistrationForm, LoginForm, PostForm, CommentForm)
from .models import User, load_user, BlogPost, Comment


@app.route('/', methods=['GET', 'POST'])
# Index will be the Home Feed that displays memes
def index():

    posts = BlogPost.objects.all()
    postList = []
    for post in posts:
        postList.append({
            'date': post.date,
            'username': post.poster.username,
            'post content': post.content, 
            'title': post.title 
            })

    return render_template('index.html', posts=postList)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()


    if form.validate_on_submit():
        print('WE GOT HERE!')
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, password=hashed)
    
        user.save()

        return redirect(url_for('login'))

    return render_template('register.html',form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    form = LoginForm()

    if form.validate_on_submit():
        print ('form validated')
        user = User.objects(username=form.username.data).first()

        if (user is not None and 
            bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('account'))

    return render_template('login.html', form=form)




@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

# Render HTML to post a meme. 
# This will contain a meme (image) upload as well as a caption (text) upload
@app.route('/post', methods=['GET', 'POST'])
@login_required
def blogpost():
    form = PostForm()
    if form.validate_on_submit():
        #user = User.objects(username=form.username.data).first()

        post = BlogPost(
            title = form.title.data,
            poster = load_user(current_user.username),
            content = form.content.data,
            date = current_time()
        ) #title, poster, post content, date

        post.save()

        return redirect(request.path)


    return render_template('post.html', form=form)

@app.route('/post/<title>', methods=['GET', 'POST'])
@login_required
def postpage(title):

    form = CommentForm()

    posts = BlogPost.objects(title=title)
    postList = []
    for post in posts:
        postList.append({
            'date': post.date,
            'username': post.poster.username,
            'content': post.content, 
            'title': post.title 
            })

    if form.validate_on_submit():
        print('WE ARE HERE')
        comment = Comment(
            user=load_user(current_user.username), 
            content=form.content.data, 
            date=current_time(),
            title=title
        )
        comment.save()
        return redirect(request.path)

    comments = Comment.objects(title=title)
    commentList = []
    for comment in comments:
        commentList.append({
            'date': comment.date,
            'username': comment.user.username,
            'content': comment.content, 
            'title': title
        })


    return render_template('blogpost.html', posts=postList, comments=commentList,form=form)




def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')