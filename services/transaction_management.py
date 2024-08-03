from models.transaction import Transaction, TransactionType, TransactionError
from models.account import Account
from services.account_management import active_accounts, load_account, get_account_by_id

from utils.file_handler import read_entire_file_as_dict
from config.settings import PATH_TO_TRANSACTIONS
from datetime import datetime


def add_transaction(user_uid, account_id, amount, transaction_type):
    # user_uid needed to group transactions in a file named with user_uid
    new_record = Transaction(
        account_id=account_id,
        user_uid=user_uid,
        amount=amount,
        transaction_type=transaction_type
    )
    account = get_account_by_id(account_id)
    if account is None:
        raise TransactionError("Trying to create transaction for user that's not logged in")
    if transaction_type == TransactionType.income:
        account.add_income(amount)
    elif transaction_type == TransactionType.expense:
        account.add_expense(amount)

    new_record.record()


def transfer_between_accounts(user_uid, account_id, other_account_id, amount):
    add_transaction(user_uid, account_id, amount, TransactionType.expense)
    add_transaction(user_uid, other_account_id, amount, TransactionType.income)


def transfer_between_users(account_id, other_username, amount):
    raise TransactionError('Cannot transfer between users!')

    # other_account = load_account(???)
    # cannot load account without user_uid
    # cannot get user_uid without user to be logged in
    # transfer should be performed to primary_account of other_username
    # cannot get primary_account without user_uid


def get_transactions(user_uid, account_id, start_date, end_date):
    record_date_list = list(read_entire_file_as_dict(PATH_TO_TRANSACTIONS + user_uid + '_transactions.json'))

    for record_date_str in record_date_list:
        record_date = datetime.strptime(record_date_str, "%d.%m.%y %H:%M:%S")
        if (record_date >= start_date) and (record_date <= end_date):
            output_record = Transaction(account_id=account_id, user_uid=user_uid)
            output_record.load()
            yield output_record



