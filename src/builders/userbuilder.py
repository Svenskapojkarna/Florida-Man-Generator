## Builder for users

## Import required libraries and classes from modules
from flask import request, Response, json
from src.builders.masonbuilder import MasonBuilder

## Set constants
MASON = "application/vnd.mason+json"

class UserBuilder(MasonBuilder):

    ## Static method to generate error message
    @staticmethod
    def create_error_response(status_code, title, message=None):
        resource_url = request.path
        body = MasonBuilder(resource_url=resource_url)
        body.add_error(title, message)
        return Response(json.dumps(body), status_code, mimetype=MASON)

    ## Statuc method to fetch the user schema
    @staticmethod
    def user_schema():
        schema = {
            "type": "object",
            "required": ["username"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "name": "username",
            "type": "string"
        }
        return schema

    ## Get all users
    def add_control_all_users(self):
        self.add_control(
            "floman:users-all",
            href='/api/articles/',
            method="GET"
        )

    ## Get a user by username
    def add_control_user_by_name(self):
        self.add_control(
            "floman:user-by-name",
            href='/api/users/<username>/',
            encoding="json",
            method='GET',
            schema=self.user_schema()
        )

    ## Get all added articles owned by a user
    def add_control_owned_article(self, username):
        self.add_control(
            "floman:owned-articles",
            href='/api/addedarticles/?owner={}'.format(username),
            method='GET'
        )

    ## Delete a user
    def add_control_delete_user(self, username):
        self.add_control(
            "floman:delete",
            href='/api/users/{}/'.format(username),
            method="DELETE"
        )

    ## Add new user
    def add_control_add_user(self):
        self.add_control(
            "floman:add-user",
            "/api/users/",
            method="POST",
            encoding="json",
            schema=self.user_schema()
        )

    ## Modify existing user
    def add_control_edit_user(self, username):
        self.add_control(
            "edit",
            href='/api/users/{}/'.format(username),
            method="PUT",
            encoding="json",
            schema=self.user_schema()
        )
