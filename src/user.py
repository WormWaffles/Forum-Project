from random import randint

class User:
    def __init__(self, username, password):
        self.id = randint(10000000, 99999999)
        self.username = username
        self.password = password
        self.user = {'id': self.id, 'username': self.username, 'password': self.password}