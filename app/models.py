from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String())
    description = db.Column(db.String(160))
    text = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def __str__(self) -> str:
        return f"{self.author_id}, {self.title}, {self.date}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    articles = db.relationship("Article")
