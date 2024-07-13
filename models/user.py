from pydantic import BaseModel
from typing import List
from hashlib import md5

from utils.file_handler import read_from_file, save_to_file, delete_from_file, FileHandlerException


class UserModel(BaseModel):
    password_hash: str
    username: str
    email: str
    account_list: List = []
    primary_account: str = ""


class User:
    """
        Описывает объект авторизованного пользователя
        md5 хэш строки username+password_hash определяет пользователя уникально (uid)
    """

    __user_data: UserModel
    __uid: str = ''
    __authorised: bool = False

    def __init__(self, username: str = '', password_hash: str = ''):
        self.__uid = self.__make_uid(username, password_hash)

    def __make_uid(self, username, password_hash) -> str:
        if (username == '') or (password_hash == ''):
            return ''

        raw_string = username + password_hash
        return md5(raw_string.encode('utf-8')).hexdigest()

    def uid(self):
        return self.__uid

    def data_model(self):
        return self.__user_data

    def login(self):
        if self.__uid == '':
            raise Exception("Log in information is not specified")
        try:
            data_model = read_from_file(filename='data/users.json', uid=self.__uid)
        except FileHandlerException as e:
            raise Exception(f'Cannot log in user {self.__user_data.username}: "{e}"')

        self.__user_data = UserModel(**data_model)
        self.__authorised = True

    def register(self, user_data: UserModel):
        self.__user_data = user_data
        self.__uid = self.__make_uid(self.__user_data.username, self.__user_data.password_hash)
        if self.__uid == '':
            raise Exception("Log in information should be specified")
        #   Create primary account  #
        self.__authorised = True

        save_to_file('data/users.json', self.__uid, self.__user_data.model_dump())

    def update_profile(self, user_data_dict: dict):
        if not self.__authorised:
            raise Exception("User is not authorised for this operation")

        prev_uid = self.__uid
        self.__user_data = UserModel(**user_data_dict)
        self.__uid = self.__make_uid(self.__user_data.username, self.__user_data.password_hash)

        if prev_uid != self.__uid:
            delete_from_file('data/users.json', prev_uid)

        save_to_file('data/users.json', self.__uid, self.__user_data.model_dump())

