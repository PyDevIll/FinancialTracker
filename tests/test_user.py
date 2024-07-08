from models.user import User, UserModel
from hashlib import md5


def test_user():
    user = User()

    # user.register
    user.register(UserModel(
        username='John Doe',
        password_hash=md5(b'1111').hexdigest(),
        email='me@gmail.com'
    ))
    assert user._User__user_data == UserModel(
        username='John Doe',
        password_hash=md5(b'1111').hexdigest(),
        email='me@gmail.com'
    )

