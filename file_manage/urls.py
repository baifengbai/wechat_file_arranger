from django.urls import path, re_path
from django.views.static import serve

from file_manage.views import verify_before_upload_file, verify_before_file_list_page, send_file_by_id, upload_file, \
    manage_wechat_group_file, deleting_wechat_group_file, edit, save_edit, ensure_delete

urlpatterns = [
    path(r'', verify_before_file_list_page),
    path(r'upload/', verify_before_upload_file),
    path(r'upload/uploading/', upload_file),
    path(r'send/', send_file_by_id),
    re_path(r'file/(?P<path>.*)', serve,
            {'document_root': 'C:/Users/Administrator/Desktop/wechat_file_arranger_v2/file/yx'}),
    path(r'manage/', manage_wechat_group_file),
    path(r'edit/', edit),
    path(r'edit/save/', save_edit),
    path(r'ensure_delete/', ensure_delete),
    path(r'delete/', deleting_wechat_group_file)
]
