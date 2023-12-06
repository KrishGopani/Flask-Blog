#helps to get current time
from datetime import datetime
from app import db

# to control the login
from app import login_manager

# is auth, is active, is anonymous, get id
# these methods are req when user login and these are included in following
from flask_login import UserMixin

# decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# importing (inheriting) from "db.Model"
class User(db.Model, UserMixin):
    # LHS represent columns, primary_key -> unique no                                        
    id = db.Column(db.Integer, primary_key=True)
    # unique-> unique name, nullable-> cannot be empty      
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # default -> will add default img later, will see use of string in img later
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #now we are relating user withs its posts
    #                       CLASS_NAME
    # "backref" is like adding another column in "Post" which tell us about the user that made that post                             
    # "lazy" -> how the data will be loaded -> here data will be loaded only if access the post
    posts = db.relationship('Post', backref='author', lazy=True)

    # this tell us how our object are printed out when we print it
    # __SOMETHINGS__ are called magic methods
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # default-> takes the current date&time
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # post is created by which user(user id)     
    # here "user.id" u is small because in the user model we're referencing the actual post class and in the foreign key we're actually referencing the table name and the column name so it's a lower case so the user model automatically has this table name set the lower case user and the post model we'll have a table name automatically set to lowercase post now if you want to set your own table names then you can set a specific table name attribute but since our models are pretty simple we'll just leave those as the default lowercase values                                       
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"