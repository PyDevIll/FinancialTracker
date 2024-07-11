from pydantic import BaseModel
import json


class FileHandlerException(Exception):
    pass


class FileHandlerNoFile(FileHandlerException):
    pass


class FileHandlerNoUID(FileHandlerException):
    pass


def __read_entire_file_as_dict(f):
    try:
        return json.loads(f.read())
    except json.decoder.JSONDecodeError:
        return {}


def save_to_file(filename: str, uid: str, data_model: BaseModel):
    with open(filename, 'r', encoding='utf8') as f:
        contents = __read_entire_file_as_dict(f)

    if uid not in contents:
        contents[uid] = {}

    contents[uid] = data_model.model_dump()

    with open(filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))


def read_from_file(filename: str, uid: str) -> dict:
    try:
        with open(filename, 'r', encoding='utf8') as f:
            contents = __read_entire_file_as_dict(f)
    except FileNotFoundError:
        raise FileHandlerNoFile(f'File {filename} not found')

    if uid not in contents:
        raise FileHandlerNoUID(f'UID "{uid}" is not present in file')

    return contents[uid]

