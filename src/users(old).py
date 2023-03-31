# from src.user import User

# _users = None

# def get_users():
#     global _users

#     class Users:
#         '''dict of users'''
#         def __init__(self):
#             self.users: dict[int, User] = {}

#         def get_all_users(self):
#             return self.users
        
#         def find_user_by_name(self, username) -> User:
#             '''Find user by name'''
#             for user in self.users.values():
#                 if user.username == username:
#                     return user
#             return None
        
#         def find_user_by_id(self, user_id) -> User:
#             '''Find user by id'''
#             for user in self.users.values():
#                 if user.id == user_id:
#                     return user
#             return None
        
#         def create_user(self, username, password) -> User:
#             '''Create new user and add to users dict'''
#             user = User(username, password)
#             self.users[user.id] = user
#             return user
        
#         def update_user(self, user_id, username, password) -> User:
#             '''Update existing user'''
#             user = self.users[user_id]
#             if not user:
#                 raise ValueError(f'user with id {user_id} not found')
#             # update user
#             self.users[user_id] = user
#             user.username = username
#             user.password = password
#             return user
        
#         def delete_user(self, user_id) -> User:
#             '''Delete existing user'''
#             user = self.users[user_id]
#             if not user:
#                 raise ValueError(f'user with id {user_id} not found')
#             del self.users[user_id]
#             return user
        
#         def clear(self) -> None:
#             '''Clear users dict'''
#             self.users.clear()

#     if _users is None:
#         _users = Users()

#     return _users