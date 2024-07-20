import json
import os


class FileHandlerException(Exception):
    pass


class FileHandlerNoFile(FileHandlerException):
    pass


class FileHandlerNoUID(FileHandlerException):
    pass


def read_entire_file_as_dict(filename) -> dict:
    try:
        with open(filename, 'r', encoding='utf8') as f:
            try:
                return json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return {}
    except FileNotFoundError:
        raise FileHandlerNoFile(f'File {filename} not found')


def save_to_file(filename: str, uid: str, data_dict: dict):
    try:
        contents = read_entire_file_as_dict(filename)
    except FileHandlerNoFile:
        contents = {}

    if uid not in contents:
        contents[uid] = {}

    contents[uid] = data_dict

    with open(filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))


def read_from_file(filename: str, uid: str) -> dict:
    contents = read_entire_file_as_dict(filename)

    if uid not in contents:
        raise FileHandlerNoUID(f'UID "{uid}" is not present in file')

    return contents[uid]


def delete_from_file(filename: str, uid: str):
    contents = read_entire_file_as_dict(filename)
    if uid not in contents:
        raise FileHandlerNoUID(f'UID "{uid}" is not present in file')

    del contents[uid]
    with open(filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))


def file_contains_key_value(filename: str, key, value):
    """
        Возвращает uid где встречается пара ключ-значение.
        Для проверки существования login'а или email'а при регистрации нового пользователя.
    """
    contents = read_entire_file_as_dict(filename)
    for _uid in contents:
        _value = contents[_uid].get(key, None)
        if _value == value:
            return _uid
    return None


def rename_file(filename: str, new_filename: str):
    contents = read_entire_file_as_dict(filename)
    with open(new_filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))

    os.remove(filename)
