import os
from typing import TextIO
from controllers.JSONFormater import convert_to_json_dict

def read_file(input_file: TextIO) -> list:
    converter = convert_to_json_dict
    return [converter(line) for line in input_file]
