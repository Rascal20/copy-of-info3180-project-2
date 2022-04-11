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
from app.models import UserProfile
from app.forms import LoginForm, RegisterForm
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

    g.current_user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/auth/login", methods=["POST"])
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
                return jsonify(data={'message': 'Login Successful','token': token, 'id': user.id})
            else:
                errors.append('Unauthorized Username or Password provided.')
        return jsonify(errors=form_errors(form) + errors)

@app.route("/api/auth/logout")
#@requires_auth
def logout():
    return jsonify(data={'message': "You've been successfully logged out."})

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'token': generate_csrf()})

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
        username = form.username.data
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
        photo.save(
                os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], photo_fn)
            )
        newUser = UserProfile(name=fullname, password=password,
                                username=username, email=email,
                                biography=bio, location=location, photo=photo_fn )
        db.session.add(newUser)
        db.session.commit()
        return jsonify(message="User created successfully."), 201
    else:
        return jsonify(form_errors(form)), 400
    


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