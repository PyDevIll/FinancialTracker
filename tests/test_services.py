from services.authentification import login, register, active_users
from hashlib import md5


def test_register():
    user = register('Somebody Someone', '123456Zz', 'a@b.c')
    assert len(active_users) == 1
    assert active_users[user.uid()].data().username == 'Somebody Someone'


def test_login():
    user = login('Somebody Someone', md5(b'123456Zz').hexdigest())
    assert len(active_users) == 1
    assert active_users[user.uid()].data().username == 'Somebody Someone'
