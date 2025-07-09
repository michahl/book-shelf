from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, UserBook, Author, Book
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .services.openlibrary import search_by_title, search_by_isbn

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
        data = request.form
        title = data.get('title')
        published_year = data.get('year')
        author_name = data.get('author')
        cover = data.get("cover")

        author = Author.query.filter_by(full_name=author_name).first()
        if not author:
            author = Author(full_name=author_name)
            db.session.add(author)
            db.session.commit()

        book = Book.query.filter_by(title=title, author_id=author.id).first()
        if not book:
            book = Book(
                title=title,
                published_year=published_year,
                cover_url=cover,
                author_id=author.id
            )
            db.session.add(book)
            db.session.commit()

        in_library = UserBook.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        if not in_library:
            in_library = UserBook(user_id=current_user.id, book_id=book.id)
            db.session.add(in_library)
            db.session.commit()

            return redirect(url_for('main.add_review', user_book_id=in_library))

        return redirect(url_for('main.library'))
    
    query = request.args.get('q')
    search_results = []
    if query:
        if query.isdigit() or query.replace("-", "").isdigit():
            data = search_by_isbn(query)
        else: 
            data = search_by_title(query)
        if data:
            search_results = data.get('docs', [])[:6]
    return render_template('new_book.html', results=search_results)

@main.route('/book/<uuid:user_book_id>/review', methods=['GET', 'POST'])
def add_review(user_book_id):
    return render_template('add_review')

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