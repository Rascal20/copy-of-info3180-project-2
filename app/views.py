"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager, csrf
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, jsonify, send_file, flash
import os
from app.models import UserProfile, Car, Favourites
from app.forms import LoginForm, RegisterForm, CarForm
from werkzeug.security import check_password_hash
from flask_wtf.csrf import generate_csrf
import jwt
from functools import wraps
from flask import _request_ctx_stack
import datetime
from werkzeug.utils import secure_filename

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)

        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        f.current_user =  payload
        return f(*args, **kwargs)

    return decorated

###
# Routing for your application.
###

@app.route('/')
def index():
    #return jsonify(message="This is the beginning of our API")
    return send_file(os.path.join('../dist/', 'index.html'))

@app.route("/api/auth/login", methods=['POST'])
def login():
    form = LoginForm()
    errors = []
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = UserProfile.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'iat': datetime.datetime.now(datetime.timezone.utc),
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
                }
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                return jsonify(data={'message': 'Login Successful','token': token, 'id': user.id}), 200
            else:
                errors.append('Unauthorized Username or Password provided.')
                return jsonify(errors=errors), 401
        return jsonify(errors=form_errors(form)), 400

@app.route("/api/auth/logout", methods=["POST"])
@requires_auth
def logout():
    return jsonify(data={'message': "You've been successfully logged out."})

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

#register a new user
#fields expected in JSON body are firstName, lastName, username, and password
@app.route('/api/register', methods=['POST'])
def registerUser():
    form = RegisterForm()
    if form.validate_on_submit():
        #userDetails = request.get_json()
        username = form.username.data
        fullname = form.fullName.data
        email = form.email.data
        location = form.location.data
        bio = form.biography.data
        photo = form.photo.data
        password = form.password.data
        #check for an existing user
        existingUser = UserProfile.query.filter_by(username=username).first()
        if existingUser:
            return jsonify(message="User already exists."), 409
        #save photo
        photo_fn = secure_filename(photo.filename)
        #photo.save(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], photo_fn))
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_fn))
        newUser = UserProfile(name=fullname, password=password,
                                username=username, email=email,
                                biography=bio, location=location, photo=photo_fn )
        db.session.add(newUser)
        db.session.commit()
        return jsonify(message="User created successfully."), 201
    else:
        return jsonify(form_errors(form)), 400

#takes the auth header and returns the user's ID  
def parse_userId(auth_header):
    token = auth_header.split()[1]
    user = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    return user['id']

@app.route('/api/cars', methods=['POST', 'GET'])
@requires_auth
def cars():
    if request.method == 'POST':
        form = CarForm()
        if form.validate_on_submit():
            make = form.make.data
            colour = form.colour.data
            model = form.model.data
            description = form.description.data
            year = form.year.data
            transmission = form.transmission.data
            car_type = form.car_type.data
            price = form.price.data
            photo = form.photo.data
            photo_fn = secure_filename(photo.filename)
            user_id = parse_userId(request.headers.get('Authorization'))
            photo.save(
                os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], photo_fn)
            )
            newCar = Car(make=make, colour=colour,
                                model=model, description=description,
                                year=year, transmission=transmission,
                                car_type=car_type, price=price,
                                photo=photo_fn, user_id=user_id)
            db.session.add(newCar)
            db.session.commit()
            return jsonify(message="Car added successfully."), 201
        else:
            return jsonify(form_errors(form)), 400
    cars = Car.query.all()
    carLst = []
    for car in cars:
        carDct = {
            'id': car.id,
            'make': car.make,
            'colour': car.colour,
            'model': car.model,
            'description': car.description,
            'year': car.year,
            'transmission': car.transmission,
            'car_type': car.car_type,
            'price': car.price,
            'photo': car.photo,
        }
        carLst.append(carDct)
    return jsonify(cars=carLst), 200

@app.route("/api/cars/<car_id>/favourite", methods=["POST"])
@requires_auth
def favourite(car_id):
    uid = parse_userId(request.headers.get('Authorization'))

    isFav = Favourites.query.filter(Favourites.car_id == car_id).filter(Favourites.user_id == uid ).first()
   
    if isFav == None:
        favourite = Favourites(car_id = car_id, user_id = uid)
        db.session.add(favourite)
        db.session.commit()
        data = {
            'message': 'Car Successfully Favourited',
            'id': car_id
        }
        return jsonify(data = data)
    return jsonify({"warning":"Car is Already a Favourite"})

@app.route("/api/cars/<car_id>/favourite/remove", methods=["POST"])
@requires_auth
def remove_favourite(car_id):
    user_id = parse_userId(request.headers.get('Authorization'))
    fav = Favourites.query.filter(Favourites.car_id == car_id).filter(Favourites.user_id == user_id ).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        data = {
            'message': 'Car Successfully Unfavourited',
            'id': car_id
        }
        return jsonify(data=data), 200
    else:
        data = {
            'message': 'Favourite not found',
            'id': car_id
        }
        return jsonify(data=data), 404


    

    

@app.route("/api/users/<user_id>", methods=["GET"])
@requires_auth
def get_user(user_id):
    user = UserProfile.query.filter_by(id = user_id).first()
    if user is None:
        return jsonify({'message': "No such user", 'errors': []})

    data = {
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'photo': "/uploads/" + user.photo,
        'email': user.email,
        'location': user.location,
        'biography': user.biography,
        'date_joined': user.date_joined
    }
    return jsonify(data=data)

@app.route("/api/cars/<car_id>", methods=["GET"])
@requires_auth
def get_car(car_id):
    car = Car.query.filter_by(id = car_id).first()
    if car is None:
        return jsonify({'message': "No such car found.", 'errors': []}), 404

    data = {
            'id': car.id,
            'make': car.make,
            'colour': car.colour,
            'model': car.model,
            'description': car.description,
            'year': car.year,
            'transmission': car.transmission,
            'car_type': car.car_type,
            'price': car.price,
            'photo': car.photo,
        }
    return jsonify(data=data)

@app.route("/api/users/<user_id>/favourites", methods=["GET"])
@requires_auth
def get_user_favourites(user_id):
    favourites = Favourites.query.filter_by(user_id=user_id).all()
    data = []

    if favourites is None:
        return jsonify({"message": "User has no favourites", 'errors': []})

    for favourite in favourites:

        car_id = favourite.car_id
        car = Car.query.filter_by(id=car_id).first()

        data.append({
            'id': car.id,
            'description': car.description,
            'year': car.year,
            'make': car.make,
            'model': car.model,
            'colour': car.colour,
            'transmission': car.transmission,
            'type': car.car_type,
            'price': car.price,
            'photo': "/uploads/"+car.photo,
            'user_id': car.user_id
        })
    return jsonify(data=data)

@app.route("/api/search", methods=["GET"])
@requires_auth
def findCars():
    searchParams = request.args
    make = searchParams.get("make")
    model = searchParams.get("model")
    if make and model:
        cars = Car.query.filter(Car.make.like(make),
                                Car.model.like(model))
    elif make:
        cars = Car.query.filter(Car.make.like(make))
    elif model:
        cars = Car.query.filter(Car.model.like(model))
    else:
        cars = Car.query.all()
    carLst = []
    for car in cars:
        carDct = {
            'id': car.id,
            'make': car.make,
            'colour': car.colour,
            'model': car.model,
            'description': car.description,
            'year': car.year,
            'transmission': car.transmission,
            'car_type': car.car_type,
            'price': car.price,
            'photo': car.photo,
        }
        carLst.append(carDct)
    return jsonify(cars=carLst), 200


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify(error="Page Not Found"), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")