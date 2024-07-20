from pydantic import BaseModel
from enum import Enum
from uuid import uuid4
from config.settings import PATH_TO_ACCOUNTS

from utils.file_handler import read_from_file, save_to_file
from utils.file_handler import FileHandlerException


class Currency(str, Enum):
    USD = 'USD'
    RUR = 'RUR'


class AccountModel(BaseModel):
    owner_uid: str
    owner_username: str = ''
    uid: str = ''
    name: str = ''
    balance: float = 0.0
    currency: Currency = Currency.RUR


class Account:
    __data: AccountModel = None

    def __init__(self, account_data: AccountModel):
        self.__data = account_data
        self.__data.uid = uuid4().hex

    def save(self):
        save_to_file(
            PATH_TO_ACCOUNTS + self.__data.owner_username + '_accounts.json',
            self.__data.uid,
            self.__data.model_dump()
        )

    def load(self, uid: str):
        try:
            account_model = read_from_file(PATH_TO_ACCOUNTS + self.__data.owner_username + '_accounts.json', uid)
        except FileHandlerException as e:
            raise Exception(f'Cannot load account info: "{e}"')

        self.__data = AccountModel(**account_model)

    def uid(self):
        return self.__data.uid

    def data(self):
        return self.__data

    def owner(self):
        return self.__data.owner_uid

    def update(self, **fields_to_update):
        updated_model = self.__data.model_dump()
        try:
            for key, value in fields_to_update.items():
                updated_model[key] = value
        except KeyError:
            raise Exception("Trying to update unexisted account field")

        self.__data = AccountModel(**updated_model)
        self.save()

    def add_income(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount. Should be greater than zero", amount)
        self.__data.balance += amount

    def add_expense(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount. Should be greater than zero", amount)
        if self.__data.balance < amount:
            raise Exception("Insufficient funds", amount)
        self.__data.balance -= amount

    def get_balance(self):
        return self.__data.balance

    def transfer(self, other_account_uid, amount):
        ...
