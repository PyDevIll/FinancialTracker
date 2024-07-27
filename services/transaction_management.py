from models.transaction import Transaction, TransactionType
from models.account import Account
from services.account_management import active_accounts, load_account

from utils.file_handler import read_entire_file_as_dict
from config.settings import PATH_TO_TRANSACTIONS
from datetime import datetime


def add_transaction(account_id, amount, transaction_type):
    new_record = Transaction(
        account_id=account_id,
        amount=amount,
        transaction_type=transaction_type
    )
    new_record.record()


def get_transactions(account_id, start_date, end_date):
    record_date_list = list(read_entire_file_as_dict(PATH_TO_TRANSACTIONS))

    for record_date_str in record_date_list:
        record_date = datetime.strptime(record_date_str, "%d.%m.%y %H:%M:%S")
        if (record_date >= start_date) and (record_date <= end_date):
            output_record = Transaction(account_id=account_id)
            output_record.load()
            yield output_record



