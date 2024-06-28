from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path("contacts/", views.contacts, name="contacts"),
    path("contact/<int:id>/", views.contact, name="contact"),
    path("contact/<int:id>/delete/", views.delete_contact, name="delete_contact"),
    path("contact/<int:id>/edit", views.edit_contact, name="edit_contact"),
    path("contacts/create/", views.create_contact, name="create_contact"),
    path("contacts/search/", views.find_contact, name="find_contact")
]