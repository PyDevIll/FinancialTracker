from models.account import Account, AccountModel
from models.user import User


def test_account_create():
    user = User('My Name', "abcxyz")
    account = Account(AccountModel(
        owner_uid=user.uid(),
        owner_username=user.username(),
        name="Основной счет"
    ))
    account.save()

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
