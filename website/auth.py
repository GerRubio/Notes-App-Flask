from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    # Get the data from the inputs.
    if request.method == 'POST':
        email = request.form.get('email')
        paswword = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, paswword):
                flash('Logged is successfully.', category = 'success')
                
                # Login.
                login_user(user, remember = True)

                # Redirect to main page when a new user is created.
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category = 'error')
        else:
            flash('E-mail does not exist.', category = 'error')

    return render_template('login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():

    # Get the data from the inputs.
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        paswword = request.form.get('password')
        passwordConf = request.form.get('passwordConf')

        user = User.query.filter_by(email = email).first()

        # Security checks.
        if user:
            flash('E-mail already exists.', category = 'error')
        elif len(email) < 4:
            flash('E-mail must be greater than 3 characters.', category = 'error')
        elif len(first_name) < 2:
            flash('Your name must be greater than 1 character.', category = 'error')
        elif paswword != passwordConf:
            flash('Passwords don\'t match.', category = 'error')
        elif len(paswword) < 7:
            flash('Password must be at least 7 characters.', category = 'error')
        else:
            new_user = User(email = email, first_name = first_name, password = generate_password_hash(paswword, method = 'sha256'))

            db.session.add(new_user)
            db.session.commit()

            # Leave me signed in after creating the account.
            login_user(new_user, remember = True)

            flash('Account created.', category = 'success')

            # Redirect to main page when new user is created.
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user = current_user)