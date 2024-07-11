from pydantic import BaseModel
from hashlib import md5


class UserModel(BaseModel):
    password_hash: str
    username: str
    email: str


class User:
    """
        Описывает объект авторизованного пользователя
        md5 хэш строки username+password_hash определяет пользователя уникально (uid)
    """

    __user_data: UserModel
    __uid: str

    def __init__(self, data_model_dict: dict):
        self.__user_data = UserModel(**data_model_dict)

    @staticmethod
    def make_uid(username: str, password_hash: str):
        raw_string = username + password_hash
        return md5(raw_string.encode('utf-8')).hexdigest()

    def uid(self):
        return self.__uid

    def data_model(self):
        return self.__user_data

    def login(self):
        ...

    def register(self, user_data: UserModel):
        ...
        # self.__user_data = user_data
        # self.__uid = User.make_uid(
        #     self.__user_data.username,
        #     self.__user_data.password_hash
        # )

    def update_profile(self, user_data: UserModel):
        self.__user_data = user_data
        self.__uid = User.make_uid(
            self.__user_data.username,
            self.__user_data.password_hash
        )
        ...
