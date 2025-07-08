from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, UserBook
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/library")
@login_required
def library():
    user_books = UserBook.query.filter_by(user_id=current_user.id).all()
    return render_template('library.html', user_books=user_books)

@main.route('/book/new', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        return redirect(url_for('main.index'))
    return render_template('new_book.html')

@main.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill out all fields')
            return redirect(url_for('main.signup'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('main.signin'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters.')
            return redirect(url_for('main.signup'))
        
        new_user = User(
            email=email, 
            password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html')

@main.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid user creditentials. Please try again!')
            return redirect(url_for('main.signin'))
        
        login_user(user)
        flash('Logged in successfully!')
        return redirect(url_for('main.index'))
        
    return render_template('auth/signin.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('main.signin'))