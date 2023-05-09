from app import app
from src.models import *
from src.users import *

def test_register(test_client):
    # Send a POST request to register a new user
    response = test_client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'confirm-password': 'testpassword'
    })

    # Check that the response redirects to the account page
    assert response.status_code == 302
    assert response.location.endswith('/account')

    # Check that the user was created in the database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'testuser@example.com'
    