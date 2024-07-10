from models.user import User, UserModel
from hashlib import md5
from utils.file_handler import save_to_file


def test_user():
    user = User()

    # user.register
    user.register(UserModel(
        username='John Doe',
        password_hash=md5(b'1111').hexdigest(),
        email='me@gmail.com'
    ))
    assert user.data_model() == UserModel(
        username='John Doe',
        password_hash=md5(b'1111').hexdigest(),
        email='me@gmail.com'
    )

    save_to_file('../data/users.json', user.uid(), user.data_model())
