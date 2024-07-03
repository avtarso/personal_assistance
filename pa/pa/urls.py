"""
URL configuration for pa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from . import views

from .api import NewsQuoteResource

news_quote_resource = NewsQuoteResource()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.main_page, name="main_page"),
    path("", include("notes.urls")),
    path("", include("contacts.urls")),
    path("users/", include("users.urls")),
    path("news/", include("news.urls")),
    path("storage/", include("storage.urls")),
    path("random_quote_api/", views.random_quote_api, name="random_quote_api"),
    path("road_map/", views.road_map, name="road_map"),

    path("reviews/", views.reviews, name="reviews"),

    re_path(r"^api/", include(news_quote_resource.urls)),
]
