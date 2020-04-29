## Resource for user collection and item

## Import required libraries and classes from modules
from flask import request, json, Response, Flask
from flask_restful import Api, Resource
from jsonschema import validate, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from src.builders.userbuilder import UserBuilder
from src.builders.masonbuilder import MasonBuilder
#added import db, otherwise adding user from apitest.py didnt work
from db.db import Users, db

## Initialize the resource
app = Flask(__name__)
api = Api(app)
CORS(app)

## Set constants
LINK_RELATIONS_URL = "/floridaman/link-relations/"
MASON = "application/vnd.mason+json"

## User collection
class UserCollection(Resource):

    ## Get all users
    def get(self):
        body = UserBuilder(items = [])
        body.add_namespace("floman", LINK_RELATIONS_URL)
        body.add_control("profile", "/profiles/articles/")
        body.add_control_user_by_name()
        body.add_control_add_user()
        for user in Users.query.all():
            item = MasonBuilder(
                username=user.username
            )
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=MASON)

    ## Add new user
    def post(self):
        if not request.json:
            return UserBuilder.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, UserBuilder.user_schema())
        except ValidationError as e:
            return UserBuilder.create_error_response(400, "Invalid JSON document", str(e))
        user = Users(
            username = request.json["username"]
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return UserBuilder.create_error_response(409, "Already exists", "User with username '{}' already exists.".format(request.json["username"]))
        return Response(status=201, headers={
            "Location": api.url_for(UserItem, username=request.json["username"])
        })

## User item
class UserItem(Resource):

    ## Get one user
    def get(self, username):
        user = Users.query.filter_by(username=username).first()
        if user is None:
            return UserBuilder.create_error_response(404, "Not found", "User with username '{}' doesn't exist.".format(username))
        body = UserBuilder(
            username=user.username
        )
        body.add_control_all_users()
        body.add_control("profile", "/profiles/users/")
        body.add_control("self", "/api/users/{}/".format(user.username))
        body.add_control_edit_user(user.username)
        body.add_control_delete_user(user.username)
        body.add_control_owned_article(user.username)
        return Response(json.dumps(body), 200, mimetype=MASON)

    ## Modify existing user
    def put(self, username):
        if not request.json:
            return UserBuilder.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, UserBuilder.user_schema())
        except ValidationError as e:
            return UserBuilder.create_error_response(400, "Invalid JSON document", str(e))
        user = Users.query.filter_by(username=username).first()
        if user is None:
            return UserBuilder.create_error_response(404, "Not found", "User with username '{}' doesn't exist.".format(username))
        user.username = request.json["username"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return UserBuilder.create_error_response(409, "Already exists", "User with username '{}' already exists.".format(request.json["username"]))
        return Response(status=204)

    ## Delete user
    def delete(self, username):
        user = Users.query.filter_by(username=username).first()
        if user is None:
            return UserBuilder.create_error_response(404, "Not found", "User with username '{}' doesn't exist.".format(username))
        db.session.delete(user)
        db.session.commit()
        return Response(status=204)
