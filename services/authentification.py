from models.user import User, UserModel
from hashlib import md5

# holds User instances for logged in users. Indexed by User.uid
active_users = {}
# holds Account instances dicts (indexed by Account.uid) for active_users. Indexed by User.uid
user_accounts = {}


def login(username, password_hash) -> User:
    user = User(username, password_hash)
    user.login()

    active_users[user.uid()] = user
    return user


def register(username, password, email) -> User:
    # create primary account and pass its uid to user.register

    user = User(username, password)
    user.register(UserModel(
        username=username,
        password_hash=md5(password.encode('utf-8')).hexdigest(),
        email=email,
        primary_account=''
    ))
    active_users[user.uid()] = user
    return user

