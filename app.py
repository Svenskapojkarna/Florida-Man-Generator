## The main Flask application to run the API

## Import required libraries and classes from modules
from flask import Flask, redirect
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from src.resources.addedarticleresource import AddedArticleCollection, AddedArticleItem
from src.resources.articleresource import ArticleCollection, ArticleItem
from src.resources.entrypoint import EntryPoint
from src.resources.userresource import UserCollection, UserItem

## Set constants
APIARY_URL = "https://floridamangenerator.docs.apiary.io/#reference/"
DATABASE_PATH = "db\\test.db"

## Initialize app configurations
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

## Set resources
api.add_resource(EntryPoint, "/api/")
api.add_resource(ArticleCollection, "/api/articles/")
api.add_resource(ArticleItem, "/api/articles/<date>/")
api.add_resource(UserCollection, "/api/users/")
api.add_resource(UserItem, "/api/users/<username>/")
api.add_resource(AddedArticleCollection, "/api/addedarticles/")
api.add_resource(AddedArticleItem, "/api/addedarticles/<int:id>/")

## Set routing to API documentation
@app.route("/floridaman/link-relations/")
def redirect_to_apiary_link_rels():
    return redirect(APIARY_URL + "link-relations")

@app.route("/profiles/articles/")
def redirect_to_articles_profile():
    return redirect(APIARY_URL + "profiles")

@app.route("/profiles/users/")
def redirect_to_users_profile():
    return redirect(APIARY_URL + "profiles")

@app.route("/profiles/addedarticles/")
def redirect_to_addedarticles_profile():
    return redirect(APIARY_URL + "profiles")
