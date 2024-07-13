import pytest

from models.user import User, UserModel
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
        user.register(UserModel(**login_info[n]))
        assert user.data_model() == UserModel(
            username=login_info[n]["username"],
            password_hash=login_info[n]["password_hash"],
            email=login_info[n]["email"],
            account_list=[],
            primary_account=""
        )

        #       User.login()
        user = User(login_info[n]["username"], login_info[n]["password_hash"])
        user.login()
        assert user.data_model() == UserModel(
            username=login_info[n]["username"],
            password_hash=login_info[n]["password_hash"],
            email=login_info[n]["email"],
            account_list=[],
            primary_account=""
        )

    # register user with same username
    new_user = User()
    with pytest.raises(Exception) as e:
        new_user.register(UserModel(**login_info[2]))

    assert str(e.value) == f'Username "{login_info[2]["username"]}" already in use'
    assert not new_user.is_authorised()
    assert new_user.data_model() is None

    # register user with same email
    new_user = User()
    login_info[2]["username"] = "Jane Dowe"
    login_info[2]["email"] = "me@gmail.com"
    with pytest.raises(Exception) as e:
        new_user.register(UserModel(**login_info[2]))

    assert str(e.value) == f'Email "{login_info[2]["email"]}" already registered by another user'
    assert not new_user.is_authorised()
    assert new_user.data_model() is None


def test_user_update_profile(login_info, users):
    # uid will change after updating
    prev_id = users[0].uid()
    login_info[0]["password_hash"] = md5(b"my_SUP3RS3C931_pw").hexdigest()

    user_data = users[0].data_model().model_dump()
    user_data["password_hash"] = login_info[0]["password_hash"]
    users[0].update_profile(user_data)
    assert prev_id != users[0].uid()

    # uid wouldn't change after updating
    prev_id = users[1].uid()
    login_info[1]["email"] = "pikachu@email.pokemon.com"

    user_data = users[1].data_model().model_dump()
    user_data["email"] = login_info[1]["email"]
    users[1].update_profile(user_data)
    assert prev_id == users[1].uid()

    for n in range(2):
        # check user_data consistency
        assert users[n].data_model() == UserModel(
            username=login_info[n]["username"],
            password_hash=login_info[n]["password_hash"],
            email=login_info[n]["email"],
            account_list=[],
            primary_account=""
        )
        # check if updated user can be logged back in
        new_user = User(login_info[n]["username"], login_info[n]["password_hash"])
        new_user.login()
        assert new_user.data_model() == UserModel(
            username=login_info[n]["username"],
            password_hash=login_info[n]["password_hash"],
            email=login_info[n]["email"],
            account_list=[],
            primary_account=""
        )

