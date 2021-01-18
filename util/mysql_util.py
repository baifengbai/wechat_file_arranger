import pymysql
import re

import traceback

db = pymysql.connect("localhost", "root", "paulniubi", "sdgs")

cursor = db.cursor()


def add_file_to_mysql(file_id: str, file_name: str, called_name: str = ''):
    sql = f"INSERT INTO `sdgs`.`file_manage_wechatgroupfile` (`file_id`, `file_name`, `called_name`) VALUES ('{file_id}', '{file_name}', '{called_name}');"
    try:
        db.ping(reconnect=True)
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False


def get_file_name_by_id(file_id: str):
    sql = f"select `file_name` from `sdgs`.`file_manage_wechatgroupfile` WHERE (`file_id` = '{file_id}')"
    try:
        db.ping(reconnect=True)
        # 执行sql语句
        cursor.execute(sql)

        row = cursor.fetchone()
        if row:
            row = row[0]
        else:
            row = ''
        return row

    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        return ''


def get_file_list_all_data():
    try:
        file_list = []
        sql = "select * from `sdgs`.`file_manage_wechatgroupfile`"

        db.ping(reconnect=True)
        cursor.execute(sql)

        num = 0
        while True:
            row = cursor.fetchone()
            if not row:
                break
            num += 1
            file_list.append({"file_id": row[0], "file_name": row[-1]})
        print('用户数:', num)
        return file_list
    except Exception as e:
        print(e)
        return []


def delete_file_info_by_id(file_id: str):
    sql = f"DELETE FROM `sdgs`.`file_manage_wechatgroupfile` WHERE (`id` = '{file_id}');"
    try:
        db.ping(reconnect=True)
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False
