import pydantic
from pydantic import BaseModel, ValidationError, PositiveFloat
from enum import Enum
from uuid import uuid4
from datetime import datetime
from config.settings import PATH_TO_TRANSACTIONS
from utils.file_handler import save_to_file, read_from_file


class TransactionError(Exception):
    ...


class TransactionType(str, Enum):
    income = 'in',
    expence = 'out'


class TransactionModel(BaseModel):
    account_id: str
    amount: PositiveFloat = 0.0
    transaction_type: TransactionType = TransactionType.income
    transaction_id: str = ''
    date: str = ''


class Transaction:
    __data: TransactionModel
    __datetime_obj: datetime = None

    def __init__(self, **init_fields):
        try:
            self.__data = TransactionModel(**init_fields)
        except ValidationError:
            raise TransactionError('Wrong transaction data')

        if "date" not in init_fields:
            self.__data.date = datetime.strftime(datetime.now(), "%d.%m.%y %H:%M:%S")

        self.__data.transaction_id = uuid4().hex

    def record(self):
        save_to_file(
            PATH_TO_TRANSACTIONS + self.__data.account_id + '_transactions.json',
            self.__data.date,
            self.__data.model_dump()
        )

    def load(self):
        transaction_model = read_from_file(
            PATH_TO_TRANSACTIONS + self.__data.account_id + '_transactions.json',
            self.__data.date
        )
        self.__data = TransactionModel(**transaction_model)

    def data(self):
        return TransactionModel(**self.__data.model_dump())

    def get_datetime(self):
        if self.__datetime_obj is None:
            self.__datetime_obj = datetime.strptime(self.__data.date, "%d.%m.%y %H:%M:%S")

        return self.__datetime_obj

