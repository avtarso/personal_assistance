# storage/urls.py
from django.urls import path
from . import views

app_name = "storage"

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete_file_confirmed/<int:file_id>/', views.delete_file_confirmed, name='delete_file_confirmed'),

    path('add_tag/', views.add_tag, name='add_tag'),
    path('tag_list/', views.tag_list, name='tag_list'),
    path('tag/<int:tag_id>', views.tag, name='tag'),
    path('tag/', views.tag_none, name='tag_none'),
    path('edit_tag/<int:tag_id>', views.edit_tag, name='edit_tag'),
    path('delete_tag/<int:tag_id>', views.delete_tag, name='delete_tag'),
    path('delete_tag_confirmed/<int:tag_id>/', views.delete_tag_confirmed, name='delete_tag_confirmed'),
    path('edit_file/<int:file_id>', views.edit_file, name='edit_file'),
    path('file/<int:file_id>', views.detail_file, name='detail_file'),

    # path('upcoming_file_review/', views.edit_file_description, name='edit_file_description'),
    # path('find/', views.find_file, name='find_file'),
]
