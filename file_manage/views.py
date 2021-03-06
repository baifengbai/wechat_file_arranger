import os
import time
from traceback import print_exc

from django.http import HttpResponse
from django.shortcuts import render
from wechat_file_arranger.settings import BASE_DIR

from file_manage.models import WechatGroupFile, GroupMember, WechatFriendInfo

from util.secret_code import decrypt_aes_func  # , encrypt_aes_func

from wechat_func import GROUP_ID, FILE_DIR_PATH, send_file

# 口令的有效时间
DELAY_ALLOWED = 600
# 文件的大小限制
FILE_SIZE_LIMIT = 52428800


# Create your views here.
def verify_before_upload_file(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s", None)
        from_whom = request.GET.get("f", '')
    else:
        secret_code = None
        from_whom = ''

    if secret_code:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if from_whom:
        from_whom_decrypted = decrypt_aes_func(from_whom)
        if not from_whom_decrypted:
            code_decrypted = None
        else:
            from_whom = from_whom_decrypted

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = int(code_decrypted)
            delay = time_now - time_code
            if delay < DELAY_ALLOWED:
                return render(request, 'yx/upload_file.html', {"from_whom": from_whom})
            else:
                return render(request, 'yx/403.html')
        except Exception as e:
            print(e)
            return HttpResponse('error')
    else:
        return render(request, 'yx/403.html')


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        try:
            my_file = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
            remark = request.POST.get("remark", '')
            from_whom = request.POST.get("from_whom", '')
            if not my_file:
                return HttpResponse("没有检测到文件!")

            from django.db import close_old_connections
            close_old_connections()
            if GroupMember.objects.filter(wx_id=from_whom):
                if WechatFriendInfo.objects.filter(wx_id=from_whom):
                    nickname = WechatFriendInfo.objects.get(wx_id=from_whom).nickname
                    if my_file.size < FILE_SIZE_LIMIT:
                        with open(
                                os.path.join(os.path.join(BASE_DIR, r"file\yx"), my_file.name),
                                'wb+') as destination:  # 打开特定的文件进行二进制的写操作
                            for chunk in my_file.chunks():  # 分块写入文件
                                destination.write(chunk)

                            WechatGroupFile.objects.create(file_name=my_file.name,
                                                           remark=remark,
                                                           uploader=from_whom,
                                                           uploader_nickname=nickname)
                        return render(request, 'yx/upload_done.html')
                    else:
                        return render(request, 'yx/file_too_large.html')

            else:
                return render(request, 'yx/403.html')
        except Exception as e:
            print(e)
            print_exc()
            return render(request, 'yx/403.html')
    else:
        return render(request, 'yx/403.html')


def verify_before_file_list_page(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s", None)
        from_whom = request.GET.get("f", '')
    else:
        secret_code = None
        from_whom = ''

    if secret_code:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if from_whom:
        from_whom_decrypted = decrypt_aes_func(from_whom)
        if not from_whom_decrypted:
            code_decrypted = None
        else:
            from_whom = from_whom_decrypted

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = int(code_decrypted)
            delay = time_now - time_code
            if delay < DELAY_ALLOWED:
                from django.db import close_old_connections
                close_old_connections()
                file_list = WechatGroupFile.objects.all().order_by('create_time__date')
                file_ls_output = []
                if file_list:
                    for file in file_list:
                        file_ls_output.append({"file_id": file.file_id,
                                               'create_time': file.create_time,
                                               'file_name': file.file_name,
                                               'remark': file.remark,
                                               'uploader_nickname': file.uploader_nickname if file.uploader_nickname else file.uploader
                                               })
                else:
                    file_ls_output = [{"file_id": '',
                                       'create_time': '',
                                       'file_name': '',
                                       'remark': '',
                                       'uploader_nickname': ''
                                       }]
                return render(request, 'yx/file_list.html',
                              {"file_list": file_ls_output, 'from': from_whom, 'secret_code': secret_code})
            else:
                return render(request, 'yx/403.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/403.html')
    else:
        return render(request, 'yx/403.html')


def send_file_by_id(request):
    if request.method == 'GET':
        try:
            file_id = request.GET.get("id")
            _to = request.GET.get("t", '')

            secret_code = request.GET.get("s", None)
            if secret_code:
                code_decrypted = decrypt_aes_func(secret_code)
            else:
                code_decrypted = None

            if _to:
                to_decrypted = decrypt_aes_func(_to)
                if not to_decrypted:
                    code_decrypted = None
                else:
                    _to = to_decrypted

            if code_decrypted:
                time_now = time.time()
                time_code = int(code_decrypted)
                delay = time_now - time_code
                if delay > DELAY_ALLOWED:
                    return render(request, 'yx/403.html')

            from django.db import close_old_connections
            close_old_connections()
            file_info = WechatGroupFile.objects.get(file_id=file_id)
            if _to == '':
                _to = GROUP_ID[0]
            file_path = os.path.join(FILE_DIR_PATH, file_info.file_name)
            result = send_file(_to, file_path)
            if result:
                return render(request, 'yx/send_done.html', {'secret_code': secret_code})
            else:
                return render(request, 'yx/error.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/error.html')
    else:
        return render(request, 'yx/error.html')


def manage_wechat_group_file(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s", None)
        from_whom = request.GET.get("f", '')
    else:
        secret_code = None
        from_whom = ''
    from_whom_origin = from_whom

    if secret_code:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if from_whom:
        from_whom_decrypted = decrypt_aes_func(from_whom)
        if not from_whom_decrypted:
            code_decrypted = None
        else:
            from_whom = from_whom_decrypted
    else:
        code_decrypted = None

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = int(code_decrypted)
            delay = time_now - time_code
            if delay < DELAY_ALLOWED:
                from django.db import close_old_connections
                close_old_connections()
                file_list = WechatGroupFile.objects.filter(uploader=from_whom).order_by('create_time__date')
                file_ls_output = []
                if file_list:
                    uploader_nickname = file_list[0].uploader_nickname
                    if not uploader_nickname:
                        uploader_nickname = file_list[0].uploader
                    for file in file_list:
                        file_ls_output.append({"file_id": file.file_id,
                                               'create_time': file.create_time,
                                               'file_name': file.file_name,
                                               'remark': file.remark,
                                               })
                else:
                    uploader_nickname = from_whom
                    file_ls_output = [{"file_id": '',
                                       'create_time': '',
                                       'file_name': '',
                                       'remark': '',
                                       }]
                return render(request, 'yx/file_manage_list.html',
                              {"file_list": file_ls_output, 'from': from_whom, "from_whom_origin": from_whom_origin,
                               'secret_code': secret_code, "uploader_nickname": uploader_nickname})
            else:
                return render(request, 'yx/403.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/403.html')
    else:
        return render(request, 'yx/403.html')


def edit(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s", None)
        file_id = request.GET.get("id", '')
        from_whom = request.GET.get("f", '')
    else:
        secret_code = None
        file_id = ''
        from_whom = ""
    from_whom_origin = from_whom

    if secret_code and file_id:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if from_whom:
        from_whom_decrypted = decrypt_aes_func(from_whom)
        if not from_whom_decrypted:
            code_decrypted = None
        else:
            from_whom = from_whom_decrypted
    else:
        code_decrypted = None

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = int(code_decrypted)
            delay = time_now - time_code
            if delay < DELAY_ALLOWED:
                from django.db import close_old_connections
                close_old_connections()
                try:
                    file_info = WechatGroupFile.objects.get(file_id=file_id)
                    user_nickname = GroupMember.objects.get(wx_id=from_whom).nickname
                except:
                    return HttpResponse("您提交的信息有误")

                return render(request, 'yx/file_info_edit.html',
                              {"file_id": file_id,
                               "user_nickname": user_nickname,
                               "secret_code": secret_code,
                               "from_whom_origin": from_whom_origin,
                               "file": {"file_name": file_info.file_name,
                                        "remark": file_info.remark,
                                        "create_time": file_info.create_time,
                                        "uploader": file_info.uploader,
                                        "uploader_nickname": file_info.uploader_nickname}})
            else:
                return render(request, 'yx/403.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/error.html')
    else:
        return render(request, 'yx/403.html')


def save_edit(request):
    if request.method == "POST":
        try:
            file_id = request.POST.get("file_id", '')
            # file_name = request.POST.get("file_name", '')
            remark = request.POST.get("remark", '')
            from django.db import close_old_connections
            close_old_connections()
            WechatGroupFile.objects.filter(file_id=file_id).update(remark=remark)
            return render(request, 'yx/update_done.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/error.html')
    else:
        return render(request, 'yx/403.html')


def ensure_delete(request):
    if request.method == 'GET':
        secret_code = request.GET.get("s", None)
        file_id = request.GET.get("id", '')
        from_whom = request.GET.get("f", '')
    else:
        secret_code = None
        file_id = ''
        from_whom = ""
    from_whom_origin = from_whom

    if secret_code and file_id:
        code_decrypted = decrypt_aes_func(secret_code)
    else:
        code_decrypted = None

    if from_whom:
        from_whom_decrypted = decrypt_aes_func(from_whom)
        if not from_whom_decrypted:
            code_decrypted = None
        else:
            from_whom = from_whom_decrypted
    else:
        code_decrypted = None

    if code_decrypted:
        time_now = time.time()
        try:
            time_code = int(code_decrypted)
            delay = time_now - time_code
            if delay < DELAY_ALLOWED:
                from django.db import close_old_connections
                close_old_connections()
                try:
                    file_info = WechatGroupFile.objects.get(file_id=file_id)
                    assert from_whom == file_info.uploader
                except:
                    return HttpResponse("您提交的信息有误")

                return render(request, 'yx/ensure_delete.html', {
                    "file_id": file_id,
                    "file_name": file_info.file_name,
                    "remark": file_info.remark,
                    "create_time": file_info.create_time,
                    "secret_code": secret_code,
                    "from_whom_origin": from_whom_origin
                })
            else:
                return render(request, 'yx/403.html')
        except Exception as e:
            print(e)
            return render(request, 'yx/error.html')
    else:
        return render(request, 'yx/403.html')


def deleting_wechat_group_file(request):
    if request.method == 'POST':
        file_id = request.POST.get("file_id", '')
        from django.db import close_old_connections
        close_old_connections()
        try:
            file_info = WechatGroupFile.objects.get(file_id=file_id)
        except:
            return HttpResponse("您提交的信息有误")

        file_path = os.path.join(FILE_DIR_PATH, file_info.file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            WechatGroupFile.objects.filter(file_id=file_id).delete()
            return render(request, 'yx/delete_done.html')
        else:
            return HttpResponse("未在本地找到此文件，删除失败")
    else:
        return render(request, 'yx/403.html')
