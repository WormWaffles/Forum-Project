import pytest
from app import app
from src.models import *

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        User.query.delete()
        Post.query.delete()
        Rating.query.delete()
        Follower.query.delete()
        Comment.query.delete()
        BusinessItems.query.delete()
        UserLikes.query.delete()
        db.session.commit()
        yield app.test_client()
