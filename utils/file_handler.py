import json


class FileHandlerException(Exception):
    pass


class FileHandlerNoFile(FileHandlerException):
    pass


class FileHandlerNoUID(FileHandlerException):
    pass


def __read_entire_file_as_dict(filename) -> dict:
    try:
        with open(filename, 'r', encoding='utf8') as f:
            try:
                return json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return {}
    except FileNotFoundError:
        raise FileHandlerNoFile(f'File {filename} not found')


def save_to_file(filename: str, uid: str, data_dict: dict):
    contents = __read_entire_file_as_dict(filename)

    if uid not in contents:
        contents[uid] = {}

    contents[uid] = data_dict

    with open(filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))


def read_from_file(filename: str, uid: str) -> dict:
    contents = __read_entire_file_as_dict(filename)

    if uid not in contents:
        raise FileHandlerNoUID(f'UID "{uid}" is not present in file')

    return contents[uid]


def delete_from_file(filename: str, uid: str):
    contents = __read_entire_file_as_dict(filename)
    if uid not in contents:
        raise FileHandlerNoUID(f'UID "{uid}" is not present in file')

    del contents[uid]
    with open(filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))
