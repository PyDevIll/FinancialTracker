from pydantic import BaseModel
from enum import Enum
from hashlib import md5

from utils.file_handler import read_from_file, save_to_file, delete_from_file, file_contains_key_value
from utils.file_handler import FileHandlerException


class Currency(str, Enum):
    USD = 'USD'
    RUR = 'RUR'


class AccountModel(BaseModel):
    name: str
    user_uid: str
    balance: float = 0.0
    currency: Currency = Currency.RUR


class Account:
    __data: AccountModel = None
    __uid: str = ''

    def __init__(self, account_data: AccountModel = None):
        self.__data = account_data
        self.__uid = self.__make_uid()

    def __make_uid(self) -> str:
        raw_string = self.__data.name + self.__data.user_uid + self.__data.currency
        return md5(raw_string.encode()).hexdigest()

    def uid(self):
        return self.__uid
