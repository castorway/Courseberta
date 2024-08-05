from flask import Blueprint, render_template, request, flash, redirect, url_for, session
# Blurprint - helps create routes for different links/paths in a web app
# render_template - renders a html file
# request - allows us to get data from a form
# flash - allows us to display messages to the user (flash a message)

from .models import User  # get the User schema to update db
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash, used for hashing password in the db for security (convert from plain text to smth else)
# check_password_hash

from . import db

from flask_login import login_user, login_required, logout_user, current_user
# current_user is connected with UserMixin

import os
from dotenv import load_dotenv
from twilio.rest import Client
# email verification with twilio, and environment variables to safely store our API keys

# creates a blueprint object of all the routes on the website
auth = Blueprint('auth', __name__)

# set up twilio api keys
load_dotenv()
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID = os.environ.get('VERIFY_SERVICE_SID')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY') 
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@auth.route('/login', methods=["GET", "POST"])
def login():
    # data = request.form  # get the data from the form, url data, etc.
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # looking for a specific entry in the db and filtering by a certain column
        user = User.query.filter_by(email=email).first()
        print(user.password, password)
        if user:
            # if a user was found with the same email check the hashed password if it matches with the entered password
            # if check_password_hash(user.password, password):
            if True:
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)  # logging in this user
                return redirect(url_for('routes.home'))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category='error')
        
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required  # makes sure the user is logged in to see the logout page
def logout():
    logout_user()  # logs the current user out
    return redirect(url_for("auth.login"))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # find if user email already exists, error
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greator than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters", category="error")
        # elif not email.endswith('@ualberta.ca'):
        #     flash("Must use a @ualberta.ca email address to sign up (ex: jsmith@ualberta.ca).", category="error")

        else:

            user_params = {
                'email' : email,
                'first_name' : first_name,
                'password' : generate_password_hash(password1, method="sha256")
            }

            session['user_params'] = user_params
            return redirect(url_for('auth.verify'))

        # return back to the signup page with any flashed error messages
        return render_template('sign_up.html', user=current_user)

    else:

        return render_template('sign_up.html', user=current_user)



@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        code = request.form['code']
        user_params = session['user_params']

        if check_verification(user_params['email'], code):
            # only if the user enters the correct code do we add the user
            
            new_user = User(**user_params)
            db.session.add(new_user)
            
            db.session.commit()
            login_user(new_user, remember=True)  # logging in this user
            flash("Account created!", category="success")
            return redirect(url_for("routes.home"))
        else:
            flash("Invalid verification code.", category="error")
            return render_template('verify.html', user=current_user)
    else:
        # send code to email submitted on signup page
        send_verification(session['user_params']['email'])
        return render_template('verify.html', user=current_user)


def send_verification(email):
    """ Send email verification code using Twilio
    """
    verification = client.verify.services(VERIFY_SERVICE_SID).verifications.create(
        to=email,
        channel='email'
    )
    print('made verification:', verification.sid, flush=True)

def check_verification(email, code):
    """ Check email verification code using Twilio
    """
    check = client.verify.services(VERIFY_SERVICE_SID).verification_checks.create(
        to=email, code=code
    )    
    return check.status == 'approved'

