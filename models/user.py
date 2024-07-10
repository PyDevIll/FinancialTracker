from pydantic import BaseModel
from hashlib import md5


class UserModel(BaseModel):
    login: str
    password_hash: str
    username: str
    email: str


class User:
    """
        Описывает объект авторизованного пользователя
        md5 хэш строки login+password_hash определяет пользователя уникально (uid)
    """

    __user_data: UserModel
    __uid: str

    def __init__(self):
        ...

    def __make_uid(self):
        raw_string = self.__user_data.login + self.__user_data.password_hash
        self.__uid = md5(raw_string.encode('utf-8')).hexdigest()

    def uid(self):
        return self.__uid

    def data_model(self):
        return self.__user_data

    def register(self, user_data: UserModel):
        self.__user_data = user_data
        self.__make_uid()

    def login(self):
        ...

    def update_profile(self, user_data: UserModel):
        self.__user_data = user_data
        self.__make_uid()
        ...
