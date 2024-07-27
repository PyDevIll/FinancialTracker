import pytest

from models.transaction import Transaction, TransactionError, TransactionType
from datetime import datetime


def test_transaction_create():
    trans = Transaction(
        account_id='abc123-id',
        amount=100.50,
        transaction_type=TransactionType.income
    )

    assert trans.get_datetime().day == datetime.now().day
    assert trans.get_datetime().hour == datetime.now().hour
    assert trans.get_datetime().minute == datetime.now().minute

    assert trans.data().transaction_type == TransactionType.income

    with pytest.raises(TransactionError):
        trans = Transaction(
            account_id='an01h39-id',
            amount=-1,
            transaction_type='in'
        )


def test_transaction_save_load():
    trans = Transaction(
        account_id='abc123-id',
        amount=100_500,
        transaction_type=TransactionType.income
    )
    trans.record()

    # date= and account_id= are used to find transaction in file
    new_trans = Transaction(
        account_id='abc123-id',
        date=trans.data().date
    )
    new_trans.load()

    # check equality of all internal __data of trans and new_trans
    assert new_trans.data() == trans.data()

    # fully identical transactions new_trans and other_trans
    # equality test should fail -> different amounts
    other_trans = Transaction(
        account_id='abc123-id',
        amount=100_500.50,
        transaction_type=TransactionType.income
    )
    other_trans._Transaction__data.transaction_id = new_trans._Transaction__data.transaction_id

    assert new_trans.data() != other_trans.data()











