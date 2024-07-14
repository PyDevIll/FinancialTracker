from pydantic import BaseModel
from enum import Enum
from hashlib import md5
from config.settings import PATH_TO_ACCOUNTS

from utils.file_handler import read_from_file, save_to_file, delete_from_file, rename_file
from utils.file_handler import FileHandlerException


class Currency(str, Enum):
    USD = 'USD'
    RUR = 'RUR'


class AccountModel(BaseModel):
    owner_uid: str
    name: str = ''
    balance: float = 0.0
    currency: Currency = Currency.RUR


class Account:
    __data: AccountModel = None
    __uid: str = ''

    def __init__(self, account_data: AccountModel = None):
        if account_data is None:
            return
        self.__data = account_data
        self.__uid = self.__make_uid()

    def __make_uid(self) -> str:
        if self.__data is None:
            return ''

        raw_string = self.__data.name + self.__data.owner_uid + self.__data.currency
        return md5(raw_string.encode()).hexdigest()

    def save(self):
        save_to_file(PATH_TO_ACCOUNTS + self.__data.owner_uid + '.json', self.__uid, self.__data.model_dump())

    def load(self, uid: str):
        try:
            account_model = read_from_file(PATH_TO_ACCOUNTS + self.__data.owner_uid + '.json', uid)
        except FileHandlerException as e:
            raise Exception(f'Cannot load account info: "{e}"')

        self.__data = AccountModel(**account_model)
        self.__uid = self.__make_uid()

    def uid(self):
        return self.__uid

    def data(self):
        return self.__data

    def update(self, **fields_to_update):
        prev_uid = self.__uid
        prev_owner_uid = self.__data.owner_uid

        updated_model = self.__data.model_dump()
        try:
            for key, value in fields_to_update.items():
                updated_model[key] = value
        except KeyError:
            raise Exception("Trying to update unexisted account field")

        self.__data = AccountModel(**updated_model)
        self.__uid = self.__make_uid()

        # Если изменилось имя или пароль владельца счета - переименовать файл счетов
        if self.__data.owner_uid != prev_owner_uid:
            rename_file(
                PATH_TO_ACCOUNTS + prev_owner_uid + '.json',
                PATH_TO_ACCOUNTS + self.__data.owner_uid + '.json'
            )
        if self.__uid != prev_uid:
            delete_from_file(PATH_TO_ACCOUNTS + self.__data.owner_uid + '.json', self.__uid)

        self.save()

