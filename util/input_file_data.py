import time
from configparser import ConfigParser, NoOptionError

conf_initial = ConfigParser()
ini_initial_path = 'util\\do_not_edit.ini'

conf = ConfigParser()
ini_path = 'file.ini'
conf.read(ini_path, encoding='utf-8')


def get_standard_time(t_delay=0):
    return time.strftime('%Y%m%d', time.localtime(time.time() + t_delay))[2:]


class DateCount:
    global conf

    def __init__(self):
        self.update()

    def update(self):
        conf_initial.read(ini_initial_path, encoding='utf-8')
        self.date = conf_initial.get('config', 'date')
        self.num_str = conf_initial.get('config', 'num')
        self.num = int(self.num_str)

        today = get_standard_time()
        if self.date == today:
            self.num += 1
            self.num_str = "{0:02d}".format(self.num)
        else:
            self.num = 1
            self.num_str = "{0:02d}".format(self.num)
            self.date = today


date_count = DateCount()


def update_conf():
    global conf
    with open(ini_path, 'w', encoding='utf-8') as ini:
        conf.write(ini)
    with open(ini_path, 'r', encoding='utf-8') as ini:
        source = ini.read()
        source = source.replace('file]', '可输入文件前的编号来查看对应文件]\n')
        with open('文件列表.txt', 'w', encoding='utf-8') as txt:
            txt.write(source)


def search_file_by_id(file_id: str):
    try:
        file_name = conf.get('file', file_id)
        return file_name
    except NoOptionError:
        return None


def delete_file_by_id(file_id: str) -> str or None:
    try:
        file_name = search_file_by_id(file_id)
        if file_name:
            conf.remove_option('file', file_id)
            update_conf()
        return file_name
    except NoOptionError:
        return None


class InputFileData:
    global date_count
    global conf
    global conf_initial

    def __init__(self, file_name: str):
        self.file_name = file_name

    def output_func(self):
        date_count.update()
        id_str = date_count.date + "{0:02d}".format(date_count.num)
        conf.set('file', id_str, self.file_name)
        update_conf()

        conf_initial.read(ini_initial_path, encoding='utf-8')
        conf_initial.set('config', "date", date_count.date)
        conf_initial.set('config', "num", date_count.num_str)


if __name__ == '__main__':
    # data = DataInputFile()
    # print(data.output_func())
    data = InputFileData("测试文件")
    data.output_func()
