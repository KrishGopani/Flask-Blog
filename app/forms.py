# pip install flask-wtf
# pip install email-validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# for custum validation to check that user doesnt register with same cred
from app.models import User

# here we check that if the updated credentials are different from the existing credential and if so then update otherwise throw message
from flask_login import current_user

# to import img for profile
from flask_wtf.file import FileField, FileAllowed
# FileField -> type of feild like - StringField
# FileAllowed -> a validator - what kind of files we allow uploading

# text are
from wtforms import TextAreaField


#create a class and which will inherit from "FlaskForm"
class RegistrationForm(FlaskForm):

    #VAR_NAME = INPUT_TYPE ("LABEL_NAME",KEYWORD=[LISTS OF NECESSARY THINGS])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #having a custum validation to check that user doesnt register with same cred
    # following is a template

    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError("Validation Message")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        #if user exist with same username it will throw an error
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

        

#create a class and which will inherit from "FlaskForm"
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # "jpg" etc type of files are allow to uploaf
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):

        # Check if the updated data is different from the existing data if yes then proceed inside the if condition
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            

# from wtforms import TextAreaField
# to create new form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')