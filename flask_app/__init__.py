from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_talisman import Talisman

import os
from datetime import datetime

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://heroku_6km76xcj:v48rkplsl0k6u11jqv47ulaur0@ds157946.mlab.com:57946/heroku_6km76xcj?retryWrites=false'
# app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/final'
app.config['SECRET_KEY'] = b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)
Talisman(app)

from . import routes