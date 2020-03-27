from flask import request, Response, json
from masonbuilder import MasonBuilder

class AddedArticleBuilder(MasonBuilder):
    @staticmethod
    def create_error_response(status_code, title, message=None):
        resource_url = request.path
        body = MasonBuilder(resource_url=resource_url)
        body.add_error(title, message)
        return Response(json.dumps(body), status_code, mimetype=MASON)

    @staticmethod
    def addedarticle_schema():
        schema = {
            "type": "object",
            "required": ["headline", "owner_username"]
        }
        props = schema["properties"] = {}
        props["date"] = {
            "type": "string"
        }
        props["link"] = {
            "type": "string"
        }
        props["headline"] = {
            "type": "string"
        }
        props["owner_username"] = {
            "type": "string"
        }
        return schema

    def add_control_all_addedarticles(self):
        self.add_control(
            "floman:addedarticles-all",
            href='/api/addedarticles/',
            method="GET"
        )

    def add_control_addedarticle_by_id(self, id):
        self.add_control(
            "floman:addedarticle-by-id",
            href='/api/addedarticles/{}/'.format(id),
            method='GET'
        )

    def add_control_owner(self, owner_username):
        self.add_control(
            "floman:owner",
            href='/api/users/?owner={}'.format(owner_username),
            method='GET'
        )

    def add_control_delete_addedarticle(self, id):
        self.add_control(
            "floman:delete",
            href='/api/addedarticles/{}/'.format(id),
            method="DELETE"
        )

    def add_control_add_addedarticle(self):
        self.add_control(
            "floman:add-addedarticle",
            "/api/addedarticles/",
            method="POST",
            encoding="json",
            schema=self.addedarticle_schema()
        )

    def add_control_edit_addedarticle(self, id):
        self.add_control(
            "edit",
            href='/api/addedarticles/{}/'.format(id),
            method="PUT",
            encoding="json",
            schema=self.addedarticle_schema()
        )