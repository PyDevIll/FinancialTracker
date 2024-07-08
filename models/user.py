from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password_hash: str
    email: str


class User:
    __user_data: UserModel

    def __init__(self):
        ...

    def register(self, user_data: UserModel):
        self.__user_data = user_data

    def login(self):
        ...

    def update_profile(self, user_data: UserModel):
        ...
