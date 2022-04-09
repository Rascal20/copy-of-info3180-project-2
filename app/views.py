"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file
import os
from app.models import UserProfile

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/login')
def login():
    return render_template('login_temp.html')
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
        #check for an existing use
        existingUser = UserProfile.query.filter_by(username=userDetails['username']).first()
        if existingUser:
            return jsonify(message="User already exists."), 409
        newUser = UserProfile(first_name=userDetails['firstName'],
                                last_name=userDetails['lastName'], username=userDetails['username'],
                                password=userDetails['password'])
        db.session.add(newUser)
        db.session.commit()
        return jsonify(message="User created successfully."), 201
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