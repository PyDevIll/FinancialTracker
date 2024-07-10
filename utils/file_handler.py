from pydantic import BaseModel
import json


def save_to_file(filename: str, uid: str, data_model: BaseModel):
    with open(filename, 'r', encoding='utf8') as f:
        try:
            contents = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            contents = {}

    if uid not in contents:
        contents[uid] = {}

    contents[uid] = data_model.model_dump()

    with open(filename, 'w', encoding='utf8') as f:
        f.write(json.dumps(contents, indent=4))

