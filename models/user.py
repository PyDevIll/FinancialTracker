from pydantic import BaseModel
from hashlib import md5
from config.settings import PATH_TO_USERS

from utils.file_handler import read_from_file, save_to_file, delete_from_file, file_contains_key_value
from utils.file_handler import FileHandlerException


class UserModel(BaseModel):
    password_hash: str
    username: str
    email: str
    primary_account: str = ""


def _check_duplicates(**user_data):
    #       проверка на использование занятого username или email
    new_username = user_data.get('username', None)
    new_email = user_data.get('email', None)

    if new_username:
        if file_contains_key_value(PATH_TO_USERS, 'username', new_username):
            raise Exception(f'Username "{new_username}" already in use')
    if new_email:
        if file_contains_key_value(PATH_TO_USERS, 'email', new_email):
            raise Exception(f'Email "{new_email}" already registered by another user')


class User:
    __data: UserModel = None
    __uid: str = ''
    __authorised: bool = False

    def __init__(self, username: str = '', password_hash: str = ''):
        self.__uid = self.__make_uid(username, password_hash)

    def __make_uid(self, username, password_hash) -> str:
        if (username == '') or (password_hash == ''):
            return ''

        raw_string = username + password_hash
        return md5(raw_string.encode('utf-8')).hexdigest()

    def __save(self):
        save_to_file(PATH_TO_USERS, self.__uid, self.__data.model_dump())

    def uid(self):
        return self.__uid

    def username(self):
        return self.__data.username

    def primary_account(self):
        return self.__data.primary_account

    def data(self):
        return self.__data

    def is_authorised(self):
        return self.__authorised

    def login(self):
        if self.__uid == '':
            raise Exception("Log in information is not specified")
        try:
            user_data = read_from_file(PATH_TO_USERS, self.__uid)
        except FileHandlerException as e:
            raise Exception(f'Cannot log in user {self.__data.username}: "{e}"')

        self.__data = UserModel(**user_data)
        self.__authorised = True

    def register(self, **user_data):
        _check_duplicates(**user_data)
        self.__data = UserModel(**user_data)
        self.__uid = self.__make_uid(self.__data.username, self.__data.password_hash)
        if self.__uid == '':
            raise Exception("Log in information should be specified")

        self.__authorised = True
        self.__save()

    def update_profile(self, **fields_to_update):
        if not self.__authorised:
            raise Exception("User is not authorised for this operation")

        _check_duplicates(**fields_to_update)

        updated_model = self.__data.model_dump()
        try:
            for key, value in fields_to_update.items():
                updated_model[key] = value
        except KeyError:
            raise Exception("Trying to update unexisted profile field")

        prev_uid = self.__uid
        self.__data = UserModel(**updated_model)
        self.__uid = self.__make_uid(self.__data.username, self.__data.password_hash)

        # If password changed - __uid() changes as well.
        # delete record with previous __uid()
        if prev_uid != self.__uid:
            delete_from_file(PATH_TO_USERS, prev_uid)

        self.__save()

    def logout(self):
        self.__authorised = False
