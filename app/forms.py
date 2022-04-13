# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField
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

class CarForm(FlaskForm):
    make = StringField('Make', validators=[InputRequired()])
    colour = StringField('Colour', validators=[InputRequired()])
    model = StringField('Model', validators=[InputRequired()])
    description =  StringField('description', widget=TextArea(), validators=[InputRequired()])
    year =  StringField('Year', validators=[InputRequired()])
    transmission =  TextField('Transmission', validators=[InputRequired()])
    car_type =  StringField('Car Type', validators=[InputRequired()])
    price =  FloatField('Price', validators=[InputRequired()])
    photo = FileField('Image', validators=[
        FileRequired(),
         FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])