import time

from util.mysql_util import *


def get_standard_time(t_delay=0):
    return time.strftime('%Y%m%d', time.localtime(time.time() + t_delay))[2:]


class DateCount:
    def __init__(self):
        self.date = get_standard_time()
        self.num_str = 0
        self.num = int(self.num_str)

    def update(self):
        self.date = get_standard_time()
        self.num += 1
        self.num_str = str(self.num)


date_count = DateCount()


class InputFileData:
    global date_count

    def __init__(self, file_name: str):
        self.file_name = file_name

    def output_func(self):
        date_count.update()
        id_str = date_count.date + "{0:02d}".format(date_count.num)
        while True:
            try:
                file_name = get_file_name_by_id(id_str)
                assert file_name != ''
            except:
                add_file_to_mysql(id_str, self.file_name)
                break
            else:
                date_count.num += 1
                id_str = date_count.date + "{0:02d}".format(date_count.num)


if __name__ == '__main__':
    # data = DataInputFile()
    # print(data.output_func())
    data = InputFileData("测试文件")
    data.output_func()
