from pydantic import BaseModel
from enum import Enum
from hashlib import md5
from config.settings import PATH_TO_ACCOUNTS

from utils.file_handler import read_from_file, save_to_file, delete_from_file, file_contains_key_value
from utils.file_handler import FileHandlerException


class Currency(str, Enum):
    USD = 'USD'
    RUR = 'RUR'


class AccountModel(BaseModel):
    name: str
    owner_uid: str
    balance: float = 0.0
    currency: Currency = Currency.RUR


class Account:
    __data: AccountModel = None
    __uid: str = ''

    def __init__(self, account_data: AccountModel = None, uid: str = ''):
        if account_data is not None:
            self.__data = account_data
            self.__uid = self.__make_uid()
            self.__save()
        elif uid != '':
            self.load(uid)

    def __make_uid(self) -> str:
        if self.__data is None:
            return ''

        raw_string = self.__data.name + self.__data.owner_uid + self.__data.currency
        return md5(raw_string.encode()).hexdigest()

    def __save(self):
        save_to_file(PATH_TO_ACCOUNTS + self.__data.owner_uid + '.json', self.__uid, self.__data.model_dump())

    def load(self, uid: str):
        try:
            account_model = read_from_file(PATH_TO_ACCOUNTS + self.__data.owner_uid, uid)
        except FileHandlerException as e:
            raise Exception(f'Cannot load account info: "{e}"')

        self.__data = AccountModel(**account_model)
        self.__uid = self.__make_uid()

    def uid(self):
        return self.__uid

    def update(self, new_name: str = '', currency: Currency = Currency.RUR):
        prev_uid = self.__uid

        if new_name != '':
            self.__data.name = new_name
        self.__data.currency = currency

        self.__uid = self.__make_uid()
        if self.__uid != prev_uid:
            delete_from_file(PATH_TO_ACCOUNTS + self.__data.owner_uid + '.json', self.__uid)

        self.__save()

