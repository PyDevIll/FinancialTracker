from models.account import Account, AccountModel, Currency
from utils.file_handler import read_entire_file_as_dict
from config.settings import PATH_TO_ACCOUNTS

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


def load_all_accounts(user_uid):
    all_accounts = read_entire_file_as_dict(PATH_TO_ACCOUNTS + user_uid + '.json')
    for acc_uid, acc_data in all_accounts.items():
        load_account(user_uid, acc_uid)


def unload_user_accounts(user_uid):
    del active_accounts[user_uid]


def update_user_accounts(user_uid, **fields_to_update):
    for acc_uid, account in active_accounts[user_uid].items():
        account.update(**fields_to_update)
