from flask import request, json, Response, Flask
from flask_restful import Api, Resource
from jsonschema import validate, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from src.builders.addedarticlebuilder import AddedArticleBuilder
from src.builders.masonbuilder import MasonBuilder
from db.db import AddedArticles

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

LINK_RELATIONS_URL = "/floridaman/link-relations/"
MASON = "application/vnd.mason+json"

class AddedArticleCollection(Resource):
    def get(self):
        body = AddedArticleBuilder(items = [])
        body.add_namespace("floman", LINK_RELATIONS_URL)
        body.add_control("profile", "/profiles/addedarticles/")
        body.add_control_add_addedarticle()
        ## Tähän tulee addedarticle-by-id
        ## Tähän tulee addedarticle-by-owner
        for article in AddedArticles.query.all():
            item = MasonBuilder(
                id=article.id,
                date=article.date,
                link=article.link,
                headline=article.headline,
                owner_username=article.owner_username
            )
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        if not request.json:
            return AddedArticleBuilder.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, AddedArticleBuilder.addedarticle_schema())
        except ValidationError as e:
            return AddedArticleBuilder.create_error_response(400, "Invalid JSON document", str(e))
        article = AddedArticles(
            date = request.json["date"],
            link = request.json["link"],
            headline = request.json["headline"],
            owner_username = request.json["owner_username"]
        )
        db.session.add(article)
        db.session.commit()
        article = AddedArticles.query.filter_by(date=request.json["date"])
        return Response(status=201, headers={
            "Location": api.url_for(AddedArticleItem, id=article.id)
        })

class AddedArticleItem(Resource):
    def get(self, id):
        article = AddedArticles.query.filter_by(id=id).first()
        if article is None:
            return AddedArticleBuilder.create_error_response(404, "Not found", "Article with ID '{}' doesn't exist.".format(id))
        body = AddedArticleBuilder(
            id=article.id,
            date=article.date,
            link=article.link,
            headline=article.headline,
            owner_username=article.owner_username
        )
        body.add_control_all_addedarticles()
        body.add_control("profile", "/profiles/addedarticles/")
        body.add_control("self", "/api/addedarticles/{}/".format(article.id))
        body.add_control_owner(article.owner_username)
        body.add_control_edit_addedarticle(article.id)
        body.add_control_delete_user(article.id)
        return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, id):
        if not request.json:
            return AddedArticleBuilder.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, AddedArticleBuilder.addedarticle_schema())
        except ValidationError as e:
            return AddedArticleBuilder.create_error_response(400, "Invalid JSON document", str(e))
        article = AddedArticles.query.filter_by(id=id).first()
        if article is None:
            return AddedArticleBuilder.create_error_response(404, "Not found", "Article with ID '{}' doesn't exist.".format(article.id))
        article.date = request.json["date"]
        article.link = request.json["link"]
        article.headline = request.json["headline"]
        article.owner_username = request.json["owner_username"]
        db.session.commit()
        return Response(status=204)

    def delete(self, id):
        article = AddedArticles.query.filter_by(id=id).first()
        if article is None:
            return AddedArticleBuilder.create_error_response(404, "Not found", "Article with ID '{}' doesn't exist.".format(article.id))
        db.session.delete(article)
        db.session.commit()
        return Response(status=204)
