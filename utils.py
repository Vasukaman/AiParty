from enum import Enum
import sys
from typing import *
import re
import csv

import os


def save_txt_file(filepath:str, text:str):
     with open(filepath, "w") as f:
             f.write(text)


def get_folder_path(filepath:str) -> str:
    
    # get the path of the script
    script_path = os.path.abspath(filepath)
    # get the folder path of the script
    folder_path = os.path.dirname(script_path)
    # print(f"Folder path {folder_path}")
    return folder_path




def check_enum_and_return_name (variable:str, enum_class:Enum):
    if variable in enum_class.__members__:
            return getattr(enum_class, variable)
    else:
            print(f"Invalid {enum_class.__name__}: {variable}")
            sys.exit()


def replace_placeholder(text:str, placeholder:str, replacement:str) -> str:
    #text = text.replace("{"+placeholder+"}", replacement)
    text = text.replace(placeholder, replacement)
    return text

def get_placeholders(string:str) -> List[str]:
    placeholders = re.findall("\{.*?\}",string)
    return placeholders
    
def csv_to_dict_list(file_path):
    dict_list = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row)
            dict_list.append(row)

    for row in dict_list:
        row["Content"].replace('\\n', '\n')

    return dict_list
