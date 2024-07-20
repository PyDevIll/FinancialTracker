from services.authentication import login, register, update_user_profile, active_users
from services.account_management import active_accounts
from models.user import User
from hashlib import md5

user: User


def test_register():
    user = register('Somebody Someone', md5(b'123456Zz').hexdigest(), 'a@b.c')
    assert len(active_users) == 1
    assert active_users[user.uid()].username() == 'Somebody Someone'


def test_login():
    global user
    user = login('Somebody Someone', md5(b'123456Zz').hexdigest())
    assert len(active_users) == 1
    assert active_users[user.uid()].username() == 'Somebody Someone'
    assert len(active_accounts) == 1
    _account = active_accounts[user.uid()][user.primary_account()]
    assert _account.owner() == user.uid()
    assert _account.uid() == user.primary_account()


def test_update_user_info():
    # поменять пароль пользователя и проверить загружаемость пользователя и счетов
    # переименуется ли файл со счетами?
    # global user

    user = login('Somebody Someone', md5(b'123456Zz').hexdigest())
    _account = active_accounts[user.uid()][user.primary_account()]
    _old_user_uid = user.uid()

    user = update_user_profile(user.uid(), password_hash=md5(b'better_password:x&8w-8gGb=@_p{]d').hexdigest())

    assert _old_user_uid != user.uid()

    assert len(active_users) == 1
    assert active_users[user.uid()].username() == 'Somebody Someone'

    assert len(active_accounts) == 1
    _account = active_accounts[user.uid()][user.primary_account()]
    assert _account.owner() == user.uid()
    assert _account.uid() == user.primary_account()


