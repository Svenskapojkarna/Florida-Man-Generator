##Based on the resource_test.py on lovelace "Testing Flask Applications part 2
from datetime import datetime
import json
#from jsonschema import validate
import os
import pytest
#import time
import tempfile

from sqlalchemy import event
from sqlalchemy.engine import Engine
#from sqlalchemy.exc import IntegrityError, StatementError

#import app and db-builder
from app import app
from db.db import db, Articles, Users, AddedArticles

## forgot what this was for?
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

## Pytest setup
@pytest.fixture
def client():   
    #clean database before running
    #(had issues with previous data)
    ##CLEANS ALL DB!
    db.drop_all()
    
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    db.create_all()
    
    populate_db()

    yield app.test_client()

    db.session.remove()

    #clean db after also, unless debugging problems in this file
    #db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_fname)

##DATABASE POPULATING
#populate database with (now with one of each only) 
def populate_db():
    _article_populate()
    _user_populate()
    _added_article_populate()

def _article_populate():
    article = Articles(
        date='01.01.2020',
        link='https://justtesting.com', 
        headline="Tests are running", 
        modtime=datetime.now()
    )
    db.session.add(article)
    db.session.commit()

def _user_populate():
    user = Users(username='user1')
    db.session.add(user)
    db.session.commit()
    
def _added_article_populate():

    addedarticle = AddedArticles(
        link='https://added.test',
        headline="This is an added article", 
        modtime=datetime.now(),
        owner_username="user1"
        #owner=Users(username="") creates new user
        #as its a link to Users table

    )
    db.session.add(addedarticle)
    db.session.commit()


### COMMON FUNCTIONS
class _TestUser:
    #create json and url for user
    def __init__(self, name):
        self.name = name
        self.url = "{}/".format(name)
        self.json = {"username":"{}".format(name)}


### TESTS
#pytest runs all function starting with "test"

def test_check_db():
    '''
    Check that the database is populated with the test data
    I don't understand what is the order of the tests
    if there is other test that adds things and doesn't remove, this may fail
    '''

    #check article
    assert Articles.query.count() == 1
    testArticle = Articles.query.first()
    assert testArticle.date == '01.01.2020'

    #check user
    assert Users.query.count() == 1
    testUser = Users.query.first()
    assert testUser.username == 'user1'

    #check added article
    assert AddedArticles.query.count() == 1
    testAdded = AddedArticles.query.first()
    assert testAdded.headline == 'This is an added article'

class TestUserCollection(object):
    '''
    Checks that the user collection work properly
    Uses _TestUser -class to simplify user creation codes
    '''

    RESOURCE_URL = "/api/users/"

    def test_post(self, client):
        '''
        Test POST-method for user
        Responses:
        415
        400
        201
        409
        Also check that the URL exists
        '''

        user1 = _TestUser("test1")
        wrongJson = {"asd":user1.name}

        ##check with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(user1.json))
        assert resp.status_code == 415

        #check without username (without data gives 415)
        resp = client.post(self.RESOURCE_URL, json=wrongJson)
        assert resp.status_code == 400

        #test with valid, verify
        resp = client.post(self.RESOURCE_URL, json=user1.json)
        assert resp.status_code == 201
        #this url should be found from 
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + user1.url)

        #check posting with the same name
        resp = client.post(self.RESOURCE_URL, json=user1.json)
        assert resp.status_code == 409

        #delete the user (otherwise messes up database query counts)
        client.delete(self.RESOURCE_URL + user1.url)
        
        
    def test_put(self, client):
        '''
        Test PUT-method for user
        Responses checked:
        404
        409
        400
        415
        204
        '''
        
        user1 = _TestUser("put1")
        user2 = _TestUser("put2")
        wrongJson = {"asd":user2.name}
        
        #add the user1 first
        client.post(self.RESOURCE_URL, json=user1.json)

        #try to modify nonexisting user
        resp = client.put(self.RESOURCE_URL + user2.url, json=user2.json)
        assert resp.status_code == 404

        #try to change name into already existing
        #add user2 for this
        client.post(self.RESOURCE_URL, json=user2.json)
        resp = client.put(self.RESOURCE_URL + user1.url, json=user2.json)
        assert resp.status_code == 409

        #remove this user2 again
        client.delete(self.RESOURCE_URL + user2.url)

        #try to put with wrong json
        resp = client.put(self.RESOURCE_URL + user1.url, json=wrongJson)
        assert resp.status_code == 400

        #try to put with wrong format
        resp = client.put(self.RESOURCE_URL + user1.url, data=json.dumps(user2.json))
        assert resp.status_code == 415

        #modify user successfully
        resp = client.put(self.RESOURCE_URL + user1.url, json=user2.json)
        assert resp.status_code == 204

        #delete the modified user (otherwise messes up database query counts)
        client.delete(self.RESOURCE_URL + user2.url)

    def test_get(self, client):
        '''
        Test GET-method for user
        responses:
        404
        200 
        '''
        
        noUser = _TestUser("get0")
        user1 = _TestUser("get1")

        #create user to test with
        client.post(self.RESOURCE_URL, json=user1.json)
        
        #try with missing user
        resp = client.get(self.RESOURCE_URL + noUser.url)
        assert resp.status_code == 404

        #try with added user
        resp = client.get(self.RESOURCE_URL + user1.url)
        assert resp.status_code == 200
        #check what is given?

        #delete the modified user (otherwise messes up database query counts)
        client.delete(self.RESOURCE_URL + user1.url)

    def test_delete(self, client):
        '''
        Test DELETE-method for user
        responses:
        404
        204 
        '''

        noUser = _TestUser("delete0")
        user1 = _TestUser("delete1")

        #create user
        client.post(self.RESOURCE_URL, json=user1.json)

        #try with missing user
        resp = client.delete(self.RESOURCE_URL + noUser.url)
        assert resp.status_code == 404

        #try with correct user
        resp = client.delete(self.RESOURCE_URL + user1.url)
        assert resp.status_code == 204