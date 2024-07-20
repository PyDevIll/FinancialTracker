from services.authentication import login, register, update_user_profile, active_users
from services.account_management import active_accounts
from hashlib import md5


def test_register():
    user = register('Somebody Someone', md5(b'123456Zz').hexdigest(), 'a@b.c')
    assert len(active_users) == 1
    assert active_users[user.uid()].username() == 'Somebody Someone'


def test_login():
    user = login('Somebody Someone', md5(b'123456Zz').hexdigest())
    assert len(active_users) == 1
    assert active_users[user.uid()].username() == 'Somebody Someone'
    assert len(active_accounts) == 1
    account = active_accounts[user.uid()][user.primary_account()]
    assert account.owner() == user.uid()
    assert account.uid() == user.primary_account()


def test_update_user_info():
    # поменять пароль пользователя и проверить загружаемость пользователя и счетов
    # переименуется ли файл со счетами?
    user = login('Somebody Someone', md5(b'123456Zz').hexdigest())

    _old_user_uid = user.uid()
    user = update_user_profile(user.uid(), password_hash=md5(b'better_password:x&8w-8gGb=@_p{]d').hexdigest())
    assert _old_user_uid != user.uid()

    assert len(active_users) == 1
    assert active_users[user.uid()].username() == 'Somebody Someone'

    assert len(active_accounts) == 1
    account = active_accounts[user.uid()][user.primary_account()]
    assert account.owner() == user.uid()
    assert account.uid() == user.primary_account()


