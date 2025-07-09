from app import db
from flask_login import UserMixin
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    is_admin = db.Column(db.Boolean, index=True, nullable=False, default=False)
    
    books = db.relationship("UserBook", back_populates='user')

    def __repr__(self):
        return f'Email: {self.email}'

class Book(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(75), nullable=False)
    published_year = db.Column(db.Integer)
    cover_url = db.Column(db.String(250))
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('author.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    author = db.relationship('Author', back_populates='books')
    users = db.relationship('UserBook', back_populates='book')

    def __repr__(self):
        return f'Book {self.title} by {self.author.full_name}'

class Author(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(75), unique=True)
    books = db.relationship("Book", back_populates="author")

    def __repr__(self):
        return f'Author: {self.full_name}'
    
class UserBook(db.Model):
    __tablename__ = 'user_book'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('book.id'), nullable=False)
    added_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # review data
    rating = db.Column(db.Integer)
    review_text = db.Column(db.Text())

    user = db.relationship('User', back_populates='books')
    book = db.relationship('Book', back_populates='users')

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'), # make sure ratings is within range
        db.UniqueConstraint('user_id', 'book_id', name='uix_user_book') # prevent duplicates
    )