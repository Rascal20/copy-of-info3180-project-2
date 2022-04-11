# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import TextArea
from wtforms import TextField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    fullName = StringField('Full name', validators=[InputRequired()])
    email =  StringField('Username', validators=[InputRequired()])
    location =  StringField('Username', validators=[InputRequired()])
    biography =  TextField('Description', widget=TextArea(), validators=[InputRequired()])
    photo = FileField('Image', validators=[
        FileRequired(),
         FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])