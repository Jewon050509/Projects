from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User

auth = Blueprint('auth', __name__)

# Route for signup page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # Receives signup info from HTML
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(username=username).first()

        # Warns user for incorrect input during signup
        if user:
            flash('Username already exists.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            # Add a new User to the database and login as the User
            new_user = User(username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.todo'))

    return render_template("signup.html", user=current_user)

# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Receives login info from HTML
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        # Display the result of login input
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.todo'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Route for logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

