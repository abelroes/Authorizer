import json


def convert_json_to_dict(text: str) -> dict:
    return json.loads(text)


def convert_dict_to_json(dictionary: dict) -> str:
    return json.dumps(dictionary)
