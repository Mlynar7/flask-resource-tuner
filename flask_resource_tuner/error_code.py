import os
import json
import random

from flask_resource_tuner.setting import Config

ERRORS = dict()
DEFAULT_SYS_ERR_FILE = "error_message/en_error_msg.json"


def load_error_code():
    sys_error_path = f"../error_message/{Config.LANGUAGE}_error_msg.json"
    sys_error = json.load(
        open(sys_error_path if os.path.exists(sys_error_path) else DEFAULT_SYS_ERR_FILE,
             "r",
             encoding="utf8"))
    if Config.ERROR_MSG_DIR:
        for e_file in os.listdir(Config.ERROR_MSG_DIR):
            if e_file.startswith(Config.LANGUAGE):
                custom_error = json.load(open(Config.ERROR_MSG_DIR + f"/{e_file}",
                                              "r",
                                              encoding="utf8"))
                same_key = set(sys_error.keys()) & set(custom_error.keys())
                if same_key:
                    raise ValueError(f"duplicate error key `{same_key}` defined in {e_file}")
                else:
                    sys_error.update(custom_error)
                    break
    else:
        global ERRORS
        ERRORS = sys_error


def is_duplicate_code(code: str):
    if not ERRORS:
        load_error_code()
    return ERRORS.get(code)


def new_error_code():
    base_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    new_code = "".join(random.sample(base_char, 9))
    while is_duplicate_code(new_code):
        return new_error_code()
    return new_code


print(new_error_code())
