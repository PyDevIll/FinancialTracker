from models.account import Account, AccountModel, Currency
from utils.file_handler import read_entire_file_as_dict
from config.settings import PATH_TO_ACCOUNTS

# Dict that holds Account instances dicts for active_users. Indexed by [User.uid][Account.uid]
active_accounts = {}


def _add_as_active(account: Account):
    if account.owner() not in active_accounts:
        active_accounts[account.owner()] = {}

    active_accounts[account.owner()][account.uid()] = account


def get_account_by_id(acc_id) -> Account:
    for user in active_accounts.keys():
        if acc_id in active_accounts[user]:
            return active_accounts[user][acc_id]


def create_account(user_uid, username, name, currency: Currency = Currency.RUR) -> Account:
    account = Account(AccountModel(
        owner_uid=user_uid,
        owner_username=username,
        name=name,
        currency=currency
    ))
    account.save()

    _add_as_active(account)

    return account


def load_account(user_uid, username, account_uid) -> Account:
    # user_uid needed to find active account in active_accounts[user_uid][acc_uid]
    account = Account(AccountModel(
        owner_uid=user_uid,
        owner_username=username
    ))
    account.load(account_uid)
    _add_as_active(account)

    return account


def load_all_accounts(user_uid, username):
    all_accounts = read_entire_file_as_dict(PATH_TO_ACCOUNTS + username + '_accounts.json')
    for acc_uid, acc_data in all_accounts.items():
        load_account(user_uid, username, acc_uid)


def unload_user_accounts(user_uid):
    del active_accounts[user_uid]


def update_user_accounts(user_uid, current_username, **fields_to_update):
    load_all_accounts(user_uid, current_username)
    for acc_uid, account in active_accounts[user_uid].items():
        account.update(**fields_to_update)
