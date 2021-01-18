import os
import time

from django.http import HttpResponse
from django.shortcuts import render

from file_manage.models import WechatGroupFile

from util.secret_code import decrypt_aes_func  # encrypt_aes_func,

from wechat_func import GROUP_ID, FILE_DIR_PATH, send_file


def send_file_yx(file_path: str, group_num: int):
    if group_num >= len(GROUP_ID):
        group_num = len(GROUP_ID) - 1
    _to = GROUP_ID[group_num]
    file_path = os.path.join(FILE_DIR_PATH, file_path)
    send_file(_to, file_path)


delay_allowed = 30000


# Create your views here.
def verify_before_upload_file(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s")
    else:
        secret_code = None

    if secret_code:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = float(code_decrypted)
            delay = time_now - time_code
            if delay < delay_allowed:
                return render(request, 'yx/upload_file.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/403.html')
    else:
        return render(request, 'yx/403.html')


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("没有检测到文件!")

        print(type(myFile.size), myFile.size)

        destination = open(
            os.path.join(r"D:\programming\python\auto_chat_robot\SDGS\wechat_file_arranger\file", myFile.name),
            'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("上传成功!")


def verify_before_file_list_page(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s")
    else:
        secret_code = None

    if secret_code:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = float(code_decrypted)
            delay = time_now - time_code
            if delay < delay_allowed:
                file_list = WechatGroupFile.objects.all()
                file_ls_output = []
                if file_list:
                    for file in file_list:
                        file_ls_output.append({"file_id": file.file_id,
                                               'create_time': file.create_time,
                                               'file_name': file.file_name,
                                               'remark': file.remark
                                               })
                else:
                    file_ls_output = [{"file_id": '',
                                       'create_time': '',
                                       'file_name': '',
                                       'remark': ''
                                       }]
                return render(request, 'yx/file_list.html', {"file_list": file_ls_output})
        except Exception as e:
            print(e)
            return render(request, 'yx/403.html')
    else:
        return render(request, 'yx/403.html')


def file_list_page(request):
    pass


def send_file_by_id(request):
    if request.method == 'GET':
        file_id = request.GET.get("id")
        file_info = WechatGroupFile.objects.get(file_id=file_id)
        send_file_yx(file_info.file_name, 0)
        return render(request, 'yx/send_done.html')
    else:
        return render(request, 'yx/error.html')
