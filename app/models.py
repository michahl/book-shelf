from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    is_admin = db.Column(db.Boolean, index=True, nullable=False)
    books = db.relationship("Book", backref='user')

    def __repr__(self):
        return f'Email: {self.email}'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), nullable=False)
    published_year = db.Column(db.Integer)
    description = db.Column(db.Text())
    isbn = db.Column(db.String(20))
    cover_url = db.Column(db.String(250))
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    reviews = db.relationship("Review", backref="book")

    def __repr__(self):
        return f'Book {self.title} by {self.author.full_name}'

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(75), unique=True)

    books = db.relationship("Book", backref="author")

    def __repr__(self):
        return f'Author: {self.full_name}'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    review_text = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    user = db.relationship("User", backref="reviews")

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'),
    )

    def __repr__(self):
        return f'Review {self.rating}/5 by {self.user.email}'
