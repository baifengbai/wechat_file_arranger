from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from file_manage.views import verify_before_upload_file, verify_before_file_list_page, send_file_by_id, upload_file

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', verify_before_file_list_page),
    path(r'upload/', verify_before_upload_file),
    path(r'upload/uploading/', upload_file),
    path(r'send/', send_file_by_id),
    re_path(r'file/(?P<path>.*)', serve,
            {'document_root': 'C:/Users/Administrator/Desktop/wechat_file_arranger_v2/file/yx'}),
]
