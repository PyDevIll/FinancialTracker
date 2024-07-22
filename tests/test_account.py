import pytest

from models.account import Account, AccountModel, AccountError
from models.user import User


def test_account_create():
    user = User('My Name', "abbefgh")
    account = Account(AccountModel(
        owner_uid=user.uid(),
        owner_username=user.username(),
        name="Основной счет"
    ))
    account.save()
    user.register(
        username=user.username(),
        password_hash=user.data().password_hash,
        email='abc@bbe.com',
        primary_account=account.uid()
    )

    assert account.data().name == "Основной счет"
    assert account.data().owner_uid == user.uid()
    assert account.data().currency == "RUR"
    assert account.data().balance == 0.0

    # Account.load()
    new_account = Account(AccountModel(
        owner_uid=user.uid(),
        owner_username=user.username()
    ))
    new_account.load(account.uid())

    assert new_account.data().name == "Основной счет"
    assert new_account.data().owner_uid == user.uid()
    assert new_account.data().currency == "RUR"
    assert new_account.data().balance == 0.0


def test_update():

    user = User('My Name', "abbefgh")
    user.login()
    account = Account(AccountModel(
        owner_uid=user.uid(),
        owner_username=user.username()
    ))
    account.load(user.primary_account())

    account.update(
        name="Yet another account",
        currency='USD'
    )
    assert account.data().name == "Yet another account"
    assert account.data().currency == "USD"

    with pytest.raises(AccountError):
        account.update(
            currency="CHF"
        )


