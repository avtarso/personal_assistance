from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("add_author/", views.add_author, name="add_author"),
    path("author_list/", views.author_list, name="author_list"),
    path("authors/<int:author_id>/", views.author_detail, name="author_detail"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("quote_list/", views.quote_list, name="quote_list"),
    path("author_quotes/<int:author_id>/", views.author_quotes, name="author_quotes"),
    path("upload_authors/", views.upload_file_authors, name="upload_authors"),
    path("upload_quotes/", views.upload_file_quotes, name="upload_quotes"),
    path("success/", views.success, name="success"),
]
