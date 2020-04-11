import os
import pytest
import tempfile
from datetime import datetime
from sqlalchemy.exc import IntegrityError

import db.db as app
from db.db import Articles, Users, AddedArticles

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    with app.app.app_context():
        app.db.create_all()
        
    yield app.db
    
    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)

# Articles table test
def test_Articles(db_handle):

    # Test entry creation
    entry = Articles(date='20.05.2011', link='https://www.google.com/', headline="First headline", modtime=datetime.now())
    db_handle.session.add(entry)
    db_handle.session.commit()
    assert Articles.query.count() == 1

    # Test getting an entry
    entry = Articles.query.filter_by(date='20.05.2011').first()
    assert entry.headline == "First headline"

    # Test deletion of an entry
    entry = Articles(date='01.01.2001', link='https://www.google.com/', headline="Second headline", modtime=datetime.now())
    db_handle.session.add(entry)
    db_handle.session.commit()
    assert Articles.query.count() == 2
    entry = Articles.query.filter_by(date='01.01.2001').first()
    db_handle.session.delete(entry)
    db_handle.session.commit()
    entry = Articles.query.first()
    assert entry.headline == "First headline"

    # Test modification of an entry
    entry = Articles.query.first()
    entry.headline = "New headline"
    db_handle.session.commit()
    entry = Articles.query.first()
    entry.headline = "New headline"

    # Test that date is unique
    entry = Articles(date='20.05.2011', link='https://www.google.com/', headline="Second headline", modtime=datetime.now())
    db_handle.session.add(entry)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

    # Test that headline can't be null
    entry = Articles.query.first()
    entry.headline = None
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

    # Test that modtime can't be null
    entry = Articles.query.first()
    entry.modtime = None
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

# Users and AddedArticles tables tests
def test_users_and_addedarticles(db_handle):
    # Test creation of new user without article
    entry = Users(username="svenskapojkarna")
    db_handle.session.add(entry)
    db_handle.session.commit()
    test = Users.query.filter_by(id=1).first()
    assert test.username == "svenskapojkarna"

    # Test deletion of a new user without article
    entry = Users(username="Matti")
    db_handle.session.add(entry)
    db_handle.session.commit()
    assert Users.query.count() == 2

    entry = Users.query.filter_by(username='Matti').first()
    db_handle.session.delete(entry)
    db_handle.session.commit()
    assert Users.query.count() == 1

    # Test modification of user without article
    entry = Users.query.filter_by(id=1).first()
    entry.username = "Elli"
    db_handle.session.commit()
    test = Users.query.filter_by(id=1).first()
    assert test.username == "Elli"

    # Test creation of an user with an article
    other = Users(username="Olli")
    db_handle.session.add(other)
    db_handle.session.commit()
    entry = AddedArticles(headline="First headline", modtime=datetime.now(), owner=other)
    db_handle.session.add(entry)
    db_handle.session.commit()
    test = Users.query.filter_by(username='Olli').first()
    test = test.article[0]
    assert test.headline == "First headline"

    # Test adding another article to exising user
    other = Users.query.filter_by(username='Olli').first()
    entry = AddedArticles(headline="Second headline", modtime=datetime.now(), owner=other)
    db_handle.session.add(entry)
    db_handle.session.commit()
    test = Users.query.filter_by(username='Olli').first()
    assert test.article[0].headline == "First headline"
    assert test.article[1].headline == "Second headline"

    # Test uniqueness of the username
    entry = Users(username="Olli")
    db_handle.session.add(entry)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    db_handle.session.rollback()

    # Test that if user is deleted, also the added articles are deleted
    assert AddedArticles.query.count() == 2
    user = Users.query.filter_by(username='Olli').first()
    assert len(user.article) == 2
    db_handle.session.delete(user)
    db_handle.session.commit()
    assert AddedArticles.query.count() == 0
