"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, jsonify, send_file, flash
import os
from app.models import UserProfile
from app.forms import LoginForm
from werkzeug.security import check_password_hash
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = UserProfile.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                flash("Login Successful.",'success')
                jsonmsg=jsonify(message=" Login Successful",token='token')         
                return jsonmsg  
        else:
            err=form_errors(form)
            for er in err:
                jsonErr=jsonify(errors=err)
            return jsonErr

@app.route("/api/auth/logout")
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('home'))

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
@app.route('/register', methods=['POST'])
def registerUser():
    if request.is_json:
        userDetails = request.get_json()
        newUser = UserProfile(first_name=userDetails['firstName'],
                                last_name=userDetails['lastName'], username=userDetails['username'],
                                password=userDetails['password'])
        db.session.add(newUser)
        db.session.commit()
        return jsonify(message="User created successfully."), 200
    return jsonify(message= "Malformed request body"), 400


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