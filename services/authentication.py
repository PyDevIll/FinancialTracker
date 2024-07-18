from models.user import User, UserModel
from models.account import Account, AccountModel
from services.account_management import create_account, load_account, unload_user_accounts

# Dict that holds User instances for logged in users. Indexed by [User.uid]
active_users = {}


def login(username, password_hash) -> User:
    user = User(username, password_hash)
    user.login()
    active_users[user.uid()] = user

    # load associated primary account
    load_account(user.uid(), user.primary_account())

    return user


def register(username, password_hash, email) -> User:
    user = User(username, password_hash)
    account = create_account(user.uid(), "Основной счет")
    user.register(UserModel(
        username=username,
        password_hash=password_hash,
        email=email,
        primary_account=account.uid()
    ))
    active_users[user.uid()] = user

    return user


def update_user_profile(user_uid, **fields_to_update):
    try:
        user: User = active_users[user_uid]
    except KeyError:
        raise Exception("User that's being updated is not logged in")

    prev_user_uid = user.uid()
    user.update_profile(**fields_to_update)

    # after password changing user and account should be reloaded.
    # accounts are reloaded during user logout-login seq
    # logout-login required to refresh active_users dict
    if prev_user_uid != user.uid():
        logout(prev_user_uid)
        # cannot login here. Username and password are not passed to this function


def logout(user_uid):
    active_users[user_uid].logout()

    del active_users[user_uid]
    unload_user_accounts(user_uid)
