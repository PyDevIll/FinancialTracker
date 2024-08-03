from models.user import User
from services.account_management import create_account, load_all_accounts, unload_user_accounts, update_user_accounts

# Dict that holds User instances for logged in users. Indexed by [User.uid]
active_users = {}


def active_user(user_uid) -> User:
    try:
        return active_users[user_uid]
    except KeyError:
        raise Exception("Trying to access not logged in user")


def login(username, password_hash) -> User:
    user = User(username, password_hash)
    user.login()
    active_users[user.uid()] = user

    # load associated primary account
    # load_account(user.uid(), user.username(), user.primary_account())

    load_all_accounts(user.uid(), username)

    return user


def register(username, password_hash, email) -> User:
    user = User(username, password_hash)
    account = create_account(user.uid(), user.username(), "Основной счет")
    user.register(
        username=username,
        password_hash=password_hash,
        email=email,
        primary_account=account.uid()
    )
    active_users[user.uid()] = user

    return user


def update_user_profile(user_uid, **fields_to_update) -> User:
    user = active_user(user_uid)

    prev_user_uid = user.uid()
    username = user.username()
    user.update_profile(**fields_to_update)

    # after password changing, user and account should be reloaded.
    # accounts are reloaded during user logout-login seq
    # logout-login required to refresh active_users dict
    if prev_user_uid != user.uid():
        update_user_accounts(prev_user_uid, username, owner_uid=user.uid())
        logout(prev_user_uid)
        user = login(username, fields_to_update["password_hash"])

    return user


def logout(user_uid):
    active_users[user_uid].logout()

    unload_user_accounts(user_uid)
    del active_users[user_uid]
