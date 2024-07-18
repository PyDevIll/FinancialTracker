from pydantic import BaseModel
from hashlib import md5
from config.settings import PATH_TO_USERS, PATH_TO_ACCOUNTS

from utils.file_handler import read_from_file, save_to_file, delete_from_file, file_contains_key_value, rename_file
from utils.file_handler import FileHandlerException


class UserModel(BaseModel):
    password_hash: str
    username: str
    email: str
    primary_account: str = ""


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

    def register(self, user_data: UserModel):
        #       проверка на использование занятого username или email
        if file_contains_key_value(PATH_TO_USERS, 'username', user_data.username):
            raise Exception(f'Username "{user_data.username}" already in use')
        if file_contains_key_value(PATH_TO_USERS, 'email', user_data.email):
            raise Exception(f'Email "{user_data.email}" already registered by another user')

        self.__data = user_data
        self.__uid = self.__make_uid(self.__data.username, self.__data.password_hash)
        if self.__uid == '':
            raise Exception("Log in information should be specified")

        self.__authorised = True
        self.__save()

    def update_profile(self, **fields_to_update):
        if not self.__authorised:
            raise Exception("User is not authorised for this operation")
        updated_model = self.__data.model_dump()
        try:
            for key, value in fields_to_update.items():
                updated_model[key] = value
        except KeyError:
            raise Exception("Trying to update unexisted profile field")

        prev_uid = self.__uid
        self.__data = UserModel(**updated_model)
        self.__uid = self.__make_uid(self.__data.username, self.__data.password_hash)

        # If password changed - User.uid() changes as well.
        if prev_uid != self.__uid:
            self.__uid_changed(prev_uid)

        self.__save()

    def __uid_changed(self, prev_uid):
        delete_from_file(PATH_TO_USERS, prev_uid)

        # Account file named with User.uid should be renamed.
        rename_file(
            PATH_TO_ACCOUNTS + prev_uid + '.json',
            PATH_TO_ACCOUNTS + self.__uid + '.json'
        )

        # owner_uid should be replaced with new one for all accounts in user accounts file
        from services.account_management import load_account
        while True:
            acc_uid = file_contains_key_value(
                PATH_TO_ACCOUNTS + self.__uid + '.json',
                'owner_uid', prev_uid
            )
            if acc_uid is None:
                break

            account = load_account(self.__uid, acc_uid)
            account.update(owner_uid=self.__uid)



    def logout(self):
        self.__authorised = False
