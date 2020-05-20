from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    email = db.EmailField(unique=True, required=True)
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    password = db.StringField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

# Caption and image
class BlogPost(db.Document):
    title = db.StringField(min_length=1, max_length=100,required=True,unique=True)
    poster = db.ReferenceField(User)
    content = db.StringField(min_length=5,required=True)
    date = db.StringField(required=True)


class Comment(db.Document):
    title = db.StringField(min_length=1, max_length=100,required=True)
    user = db.ReferenceField(User)
    content = db.StringField(min_length=5,max_length=500,required=True)
    date = db.StringField(required=True)

