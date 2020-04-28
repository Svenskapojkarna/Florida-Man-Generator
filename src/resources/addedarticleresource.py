## Resources for Added article collection and Added Article item

## Import required libraries and classes from modules
from flask import request, json, Response, Flask
from flask_restful import Api, Resource
from jsonschema import validate, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from src.builders.addedarticlebuilder import AddedArticleBuilder
from src.builders.masonbuilder import MasonBuilder
from db.db import db, AddedArticles

## Set constants
LINK_RELATIONS_URL = "/floridaman/link-relations/"
MASON = "application/vnd.mason+json"

## Initialize the resource
app = Flask(__name__)
api = Api(app)

## Added Article collection
class AddedArticleCollection(Resource):

    ## Get added article collection
    def get(self):
        body = AddedArticleBuilder(items = [])
        body.add_namespace("floman", LINK_RELATIONS_URL)
        body.add_control("profile", "/profiles/addedarticles/")
        body.add_control_add_addedarticle()
        body.add_control_addedarticle_by_id()
        body.add_control_addedarticle_by_owner()
        owner = request.args.get('owner')
        if owner:
            for article in AddedArticles.query.filter_by(owner_username=owner):
                item = MasonBuilder(
                    id=article.id,
                    link=article.link,
                    headline=article.headline,
                    owner_username=article.owner_username
                )
                body["items"].append(item)
        else:
            for article in AddedArticles.query.all():
                item = MasonBuilder(
                    id=article.id,
                    link=article.link,
                    headline=article.headline,
                    owner_username=article.owner_username
                )
                body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=MASON)

    ## Add a new added article
    def post(self):
        if not request.json:
            return AddedArticleBuilder.create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, AddedArticleBuilder.addedarticle_schema())
        except ValidationError as e:
            return AddedArticleBuilder.create_error_response(400, "Invalid JSON document", str(e))
        article = AddedArticles(
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

## Added Article item
class AddedArticleItem(Resource):

    ## Get one added article
    def get(self, id):
        article = AddedArticles.query.filter_by(id=id).first()
        if article is None:
            return AddedArticleBuilder.create_error_response(404, "Not found", "Article with ID '{}' doesn't exist.".format(id))
        body = AddedArticleBuilder(
            id=article.id,
            link=article.link,
            headline=article.headline,
            owner_username=article.owner_username
        )
        body.add_control_all_addedarticles()
        body.add_control("profile", "/profiles/addedarticles/")
        body.add_control("self", "/api/addedarticles/{}/".format(article.id))
        body.add_control_edit_addedarticle(article.id)
        body.add_control_delete_addedarticle(article.id)
        return Response(json.dumps(body), 200, mimetype=MASON)

    ## Edit an added article
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
        article.link = request.json["link"]
        article.headline = request.json["headline"]
        article.owner_username = request.json["owner_username"]
        db.session.commit()
        return Response(status=204)

    ## Delete an added article
    def delete(self, id):
        article = AddedArticles.query.filter_by(id=id).first()
        if article is None:
            return AddedArticleBuilder.create_error_response(404, "Not found", "Article with ID '{}' doesn't exist.".format(article.id))
        db.session.delete(article)
        db.session.commit()
        return Response(status=204)
