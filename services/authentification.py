from models.user import User, UserModel
from models.account import Account, AccountModel
from hashlib import md5

# Dict that holds User instances for logged in users. Indexed by User.uid
active_users = {}
# Dict that holds Account instances dicts (indexed by Account.uid) for active_users. Indexed by User.uid
active_user_accounts = {}


def login(username, password_hash) -> User:
    user = User(username, password_hash)
    user.login()

    # load associated primary account
    account = Account(AccountModel(
        owner_uid=user.uid()
    ))
    account.load(user.primary_account())

    active_users[user.uid()] = user
    if user.uid() not in active_user_accounts:
        active_user_accounts[user.uid()] = {}
    active_user_accounts[user.uid()][account.uid()] = account

    return user


def register(username, password, email) -> User:
    user = User(username, password)
    user.register(UserModel(
        username=username,
        password_hash=md5(password.encode('utf-8')).hexdigest(),
        email=email,
        primary_account=''
    ))
    account = Account(AccountModel(
        owner_uid=user.uid(),
        name="Основной счет"
    ))
    user.update_profile(primary_account=account.uid())

    active_users[user.uid()] = user
    if user.uid() not in active_user_accounts:
        active_user_accounts[user.uid()] = {}
    active_user_accounts[user.uid()][account.uid()] = account

    return user

