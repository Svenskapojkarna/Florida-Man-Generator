from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(32), unique=True, nullable=False)
    link = db.Column(db.String(256), nullable=True)
    headline = db.Column(db.String(128), nullable=False)
    modtime = db.Column(db.DateTime, nullable=False)

class AddedArticles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(256), nullable=True)
    headline = db.Column(db.String(128), nullable=False)
    modtime = db.Column(db.DateTime, nullable=False)
    owner_username = db.Column(db.String(32), db.ForeignKey("users.username", ondelete="CASCADE"))
    owner = db.relationship("Users", back_populates="article")

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    article = db.relationship("AddedArticles", back_populates="owner", cascade="all, delete-orphan")
