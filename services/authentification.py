from models.user import User
from utils.file_handler import read_from_file, FileHandlerException


def login(username, password_hash) -> User:
    try:
        data_model = read_from_file(
            filename='../data/users.json',
            uid=User.make_uid(username, password_hash),
        )
    except FileHandlerException as e:
        raise Exception(f'Cannot log in user {username}: "{e}"')

    return User(data_model)
