from . import db
from werkzeug.security import generate_password_hash


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))
    email = db.Column(db.String(80))
    photo = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime, server_default=db.func.now())
    biography = db.Column(db.String(255))

    def __init__(self, name, email, username, password, location,
                biography, photo):
        self.name = name
        self.email = email
        self.photo = photo
        self.location = location
        self.biography = biography
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    colour = db.Column(db.String(80))
    photo = db.Column(db.String(80))
    description = db.Column(db.String(255))
    year = db.Column(db.String(80))
    transmission = db.Column(db.String(80))
    car_type = db.Column(db.String(80))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer)


    def __init__(self, make, colour, model, description, year,
                transmission, photo,car_type, price, user_id):
        self.make = make
        self.colour = colour
        self.model = model
        self.photo = photo
        self.description = description
        self.year = year
        self.transmission = transmission
        self.car_type = car_type
        self.price = price
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Car %r>' % (self.id)


class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self,car_id,user_id):
        self.car_id = car_id
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Car ID %r>' % self.car_id