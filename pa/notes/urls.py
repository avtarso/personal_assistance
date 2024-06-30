from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("all-notes/", views.all_notes, name="all_notes"),
    path("add-note/", views.add_note, name="add_note"),
    path("note/<int:id>/", views.note, name="note"),
    path("note/<int:id>/edit/", views.edit_note, name="edit_note"),
    path("note/<int:id>/delete/", views.delete_note, name="delete_note"),
    path("find-notes/", views.find_notes, name="find_notes"),
    path("by-name/", views.by_name, name="by_name"),
    path("by-tag/", views.by_tag, name="by_tag"),
    path("all-notes/tag/<str:name>", views.by_tag_name, name="by_tag_name")
]