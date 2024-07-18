from models.account import Account, AccountModel, Currency
from models.user import User

# Dict that holds Account instances dicts for active_users. Indexed by [User.uid][Account.uid]
active_accounts = {}


def _add_as_active(account: Account):
    if account.owner() not in active_accounts:
        active_accounts[account.owner()] = {}

    active_accounts[account.owner()][account.uid()] = account


def create_account(user_uid, name, currency: Currency = Currency.RUR) -> Account:
    _account = Account(AccountModel(
        owner_uid=user_uid,
        name=name,
        currency=currency
    ))
    _account.save()

    _add_as_active(_account)

    return _account


def load_account(user_uid, account_uid) -> Account:
    _account = Account(AccountModel(
        owner_uid=user_uid
    ))
    _account.load(account_uid)
    _add_as_active(_account)

    return _account


def unload_user_accounts(user_uid):
    del active_accounts[user_uid]

