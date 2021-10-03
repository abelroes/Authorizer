from typing import List
from controllers.formaters.JSONFormater import convert_dict_to_json

def format_output(list_to_output: List[dict]) -> str:
    return ''.join(map(lambda item: f"{convert_dict_to_json(item)}\n", list_to_output))