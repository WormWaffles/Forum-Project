from app import app
from src.models import *
from src.users import *
from src.user_follow import *

def test_follow_user(test_client):
    db.create_all()
    user1 = User(user_id=111111, username='John', email='john@email.com', password='password', private=False, is_business=False)
    user2 = User(user_id=222222, username='Jane', email='jane@email.com', password='password', private=False, is_business=False)
    db.session.add_all([user1, user2])
    db.session.commit()

    result = Follows.foo_followed_bar(user1.user_id, user2.user_id)
    assert result == 99

# def test_follow_user():
#     # Create a test database and add some users to it
#     db.create_all()
#     user1 = User(username='user1', profile_pic='pic1.jpg')
#     user2 = User(username='user2', profile_pic='pic2.jpg')
#     db.session.add_all([user1, user2])
#     db.session.commit()
    
#     # Follow user2 from user1
#     result = follows.foo_followed_bar(user1.user_id, user2.user_id)
#     assert result == 99
    
#     # Verify that the follow relationship was created in the database
#     follow = Follower.query.filter_by(follower_user_id=user1.user_id, followed_user_id=user2.user_id).first()
#     assert follow is not None
    
#     # Try to follow user2 from user1 again (this should fail)
#     result = follows.foo_followed_bar(user1.user_id, user2.user_id)
#     assert result == 99
    
#     # Unfollow user2 from user1
#     result = follows.foo_unfollowed_bar(user1.user_id, user2.user_id)
#     assert result == -99
    
#     # Verify that the follow relationship was removed from the database
#     follow = Follower.query.filter_by(follower_user_id=user1.user_id, followed_user_id=user2.user_id).first()
#     assert follow is None
    
#     # Clean up the test database
#     db.session.rollback()
#     db.drop_all()