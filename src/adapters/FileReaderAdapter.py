import os
from typing import TextIO
from controllers.JSONFormater import convert_to_json_dict

def read_file(input_file: TextIO) -> list:
    file_in_lines_list = []
    converter = convert_to_json_dict
    for line in input_file:
        file_in_lines_list.append(converter(line))
    return file_in_lines_list
