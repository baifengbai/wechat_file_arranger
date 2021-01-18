import time
import os
import shutil
from loguru import logger
import traceback

from util.operate_file import InputFileData

PROJECT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def move_wechat_file(file):
    try:
        if not os.path.isfile(file):
            # print("%s not exist!" % file)
            return False
        else:
            fpath, fname = os.path.split(file)  # 分离文件名和路径
            dst_path = os.path.join(os.path.join(PROJECT_DIR_PATH, 'file'))
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)  # 创建路径
            shutil.move(file, os.path.join(dst_path, fname))  # 移动文件
            logger.info("move %s -> %s" % (file, os.path.join(dst_path, fname)))
            return True
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        return False


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
