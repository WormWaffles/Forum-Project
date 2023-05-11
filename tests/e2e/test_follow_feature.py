from app import app
from src.models import *
from src.users import *

def test_follow_button(test_client):
    # Create users
    user1 = User(user_id=111111, username='John', email='john@email.com', password='password', private=False, is_business=False)
    user2 = User(user_id=222222, username='Jane', email='jane@email.com', password='password', private=False, is_business=False)
    business = User(user_id=333333, username='Barhops', email='barhops@email.com', password='password', private=False, is_business=True);
    
    db.session.add(user1)
    
    # # Test users following users
    # foo_followed_bar(user1.user_id,user2.user_id)
    # response = test_client.post('/follow/222222?is_Following=True')
    # assert response.status_code == 302
    # # Test users following businesses


    # # Click on follow button on user profile page
    # # set up test data and context
    # with self.client:
    #     # log in as a user
    #     self.client.post('/login', data=dict(
    #         username='test_user',
    #         password='password'
    #     ), follow_redirects=True)
        
    #     # call the follow endpoint
    #     response = self.client.post('/follow/1')
        
    #     # assert that the response is a redirect to the view_user endpoint
    #     self.assertRedirects(response, '/view_user/1?is_Following=True')
        
    #     # assert that the foo_followed_bar method was called with the correct arguments
    #     # Follows.foo_followed_bar.assert_called_with(g.user, g.user.user_id, 1)

    
