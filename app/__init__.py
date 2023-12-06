# importing flask
from flask import Flask
#⭐⭐⭐⭐
# flash is use to display a msg



# will help in Database
# pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# for hashing the pass
from flask_bcrypt import Bcrypt

# for login
from flask_login import LoginManager


# creating an instance using variable "app"
app = Flask(__name__)

# setting secret key -> they can be get of random number
# to generate secret key go to terminal -> python -> import secrets -> secrets.token_hex(16) -> exit()
app.config["SECRET_KEY"]='6c7bd5020d4242dd5364c0b96ae9d234'  
#⭐⭐⭐⭐

# Url where database is located and we are using SQLite as DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# instance of our DB
db = SQLAlchemy(app)

# manually push an application context in a Flask application
app.app_context().push()


# initialize
bcrypt = Bcrypt(app)

#instance
login_manager = LoginManager(app)

# idk
login_manager.login_view = 'login'
# 'login' fxn name of our route

# this immproves how flash msg are displayed
# 'info' is a bootstrap class
login_manager.login_message_category = 'info'



from app import routes