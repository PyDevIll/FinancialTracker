from models.user import User, UserModel
from hashlib import md5

active_users = {}


def login(username, password_hash) -> User:
    # global active_users
    user = User(username, password_hash)
    user.login()

    active_users[user.uid()] = user
    return user


def register(username, password, email) -> User:
    # global active_users
    #   check for login and email availability  #
    user = User(username, password)
    user.register(UserModel(
        username=username,
        password_hash=md5(password.encode('utf-8')).hexdigest(),
        email=email
    ))

    active_users[user.uid()] = user
    return user

