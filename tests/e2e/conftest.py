import pytest
from app import app
from src.models import *  #import all db objects? i.e. Users, Rating, Post_Feed, etc.?

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        User.query.delete()
        db.session.commit()
        yield app.test_client()
