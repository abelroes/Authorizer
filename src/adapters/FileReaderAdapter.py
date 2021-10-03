from typing import List, TextIO
from controllers.formaters.JSONFormater import convert_json_to_dict


def read_file(input_file: TextIO) -> List[dict]:
    converter = convert_json_to_dict
    return [converter(line) for line in input_file]
