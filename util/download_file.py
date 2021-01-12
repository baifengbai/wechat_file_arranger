import os
import time

from util.input_file_data import InputFileData
from util.operate_file import move_wechat_file

if_downloading_file = 0


def download_file(file_path):
    global if_downloading_file
    if_succeed = False
    try_times = 0
    while if_downloading_file:
        time.sleep(2)

    if_downloading_file = 1
    while not if_succeed and try_times <= 30:
        if_succeed = move_wechat_file(file_path)
        if if_succeed:
            file_name = os.path.split(file_path)[1]
            input_file_data_instance = InputFileData(file_name)
            input_file_data_instance.output_func()
            try_times += 1
            time.sleep(1)
        else:
            time.sleep(2)
    if_downloading_file = 0

    if if_succeed:
        return True
    else:
        return False
