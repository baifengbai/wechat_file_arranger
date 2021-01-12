import os
import shutil
from loguru import logger
import traceback
# import time

PROJECT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def move_wechat_file(file):
    try:
        if not os.path.isfile(file):
            print("%s not exist!" % file)
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
