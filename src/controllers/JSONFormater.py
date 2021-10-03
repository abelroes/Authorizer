import json


def convert_to_json_dict(text: str) -> dict:
    return json.loads(text)