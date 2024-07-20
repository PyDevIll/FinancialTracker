import pytest

from models.user import User
from hashlib import md5

user_list = [User(), User()]


@pytest.fixture
def login_info():
    return [
        {
            'username': 'John Doe',
            'password_hash': md5(b'1111').hexdigest(),
            'email': 'me@gmail.com'
        },
        {
            'username': 'Pikachu #25',
            'password_hash': md5(b'pikaP1ka').hexdigest(),
            'email': 'pokemon@email.pokemon.com'
        },
        {
            'username': 'John Doe',
            'password_hash': md5(b'ImNewUser111').hexdigest(),
            'email': 'him@gmail.com'
        },
    ]


@pytest.fixture
def users():
    return user_list


def test_user_register_login(login_info, users):
    for n, user in enumerate(users):
        #       User.register()
        user.register(**login_info[n])
        assert user.data().username == login_info[n]["username"]
        assert user.data().password_hash == login_info[n]["password_hash"]
        assert user.data().email == login_info[n]["email"]

        #       User.login()
        user = User(login_info[n]["username"], login_info[n]["password_hash"])
        user.login()
        assert user.data().username == login_info[n]["username"]
        assert user.data().password_hash == login_info[n]["password_hash"]
        assert user.data().email == login_info[n]["email"]

        # register user with same username
    new_user = User()
    with pytest.raises(Exception) as e:
        new_user.register(**login_info[2])

    assert str(e.value) == f'Username "{login_info[2]["username"]}" already in use'
    assert not new_user.is_authorised()
    assert new_user.data() is None

    # register user with same email
    new_user = User()
    login_info[2]["username"] = "Jane Dowe"
    login_info[2]["email"] = "me@gmail.com"
    with pytest.raises(Exception) as e:
        new_user.register(**login_info[2])

    assert str(e.value) == f'Email "{login_info[2]["email"]}" already registered by another user'
    assert not new_user.is_authorised()
    assert new_user.data() is None


def test_user_update_profile(login_info, users):
    users[0] = User(login_info[0]["username"], login_info[0]["password_hash"])
    users[0].login()
    users[1] = User(login_info[1]["username"], login_info[1]["password_hash"])
    users[1].login()

    # uid will change after updating
    prev_id = users[0].uid()
    login_info[0]["password_hash"] = md5(b"my_SUP3RS3C931_pw").hexdigest()
    users[0].update_profile(password_hash=login_info[0]["password_hash"])
    assert prev_id != users[0].uid()

    # uid wouldn't change after updating
    prev_id = users[1].uid()
    login_info[1]["email"] = "pikachu@email.pokemon.com"
    users[1].update_profile(email=login_info[1]["email"])
    assert prev_id == users[1].uid()

    for n in range(2):
        # check user.data consistency
        assert users[n].data().username == login_info[n]["username"]
        assert users[n].data().password_hash == login_info[n]["password_hash"]
        assert users[n].data().email == login_info[n]["email"]

        # check if updated user can be logged back in
        new_user = User(login_info[n]["username"], login_info[n]["password_hash"])
        new_user.login()
        assert new_user.data().username == login_info[n]["username"]
        assert new_user.data().password_hash == login_info[n]["password_hash"]
        assert new_user.data().email == login_info[n]["email"]

