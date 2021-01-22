import binascii

import time
import os
import shutil
from loguru import logger
import traceback


def parse_dat_to_xor_code(dat_path: str) -> int:
    try:
        with open(dat_path, 'rb') as shit:
            shi = shit.read(2)
            cooked_shi = binascii.b2a_hex(shi).decode('UTF-8')
            return eval('0x' + hex(eval('0x' + cooked_shi) ^ 0xFFD8)[-2:])
    except Exception as e:
        print(e)
        return 0


PROJECT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def move_wechat_file(file):
    try:
        if not os.path.isfile(file):
            # print("%s not exist!" % file)
            return False
        else:
            fpath, fname = os.path.split(file)  # 分离文件名和路径
            dst_path = os.path.join(os.path.join(PROJECT_DIR_PATH, r'file\yx'))
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
        time.sleep(2)
    if_downloading_file = 0

    if if_succeed:
        return True
    else:
        return False


if __name__ == '__main__':
    dir_path = r'C:\Users\Administrator\Documents\WeChat Files\wxid_**************\FileStorage\Image\2021-01'
    name = 'e486fd828991955ea48bfe2bbeaf****.dat'
    xor_code = parse_dat_to_xor_code(os.path.join(dir_path, name))
    print(xor_code)
    print(hex(int(time.time()*100))[2:])
